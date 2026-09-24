"""Polite async HTTP client shared by every case.

What it guarantees, in order:

1. robots.txt is honored, including ``Crawl-delay`` (RFC 9309: a 4xx robots.txt means
   no rules, a 5xx or unreachable one means stay out).
2. Each host gets a minimum interval between requests, no matter how many tasks are in flight.
3. Transient failures (429, 5xx, timeouts, dropped connections) are retried with exponential
   backoff and jitter; a ``Retry-After`` header from the server always wins.
4. An anti-bot wall stops the run: once a host shows a challenge page, every later request to
   that host fails fast without touching the network. The kit never tries to get around it.
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import time
from collections import Counter
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import httpx

log = logging.getLogger("wdk.fetch")

DEFAULT_USER_AGENT = "webdata-delivery-kit/0.1 (+https://github.com/Jsebastian323/webdata-delivery-kit)"
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
_BLOCK_MARKERS = (
    "captcha",
    "cf-chl",
    "challenge-platform",
    "attention required",
    "unusual traffic",
    "are you a robot",
)


class FetchError(RuntimeError):
    """The request failed for good (after retries, or with a non-retryable status)."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class RobotsDisallowed(FetchError):
    """robots.txt does not allow this URL for our user agent."""


class Blocked(FetchError):
    """The response is an anti-bot wall. The run stops here on purpose."""


@dataclass
class FetchStats:
    requests: int = 0
    robots_requests: int = 0
    retries: int = 0
    failures: int = 0
    bytes_received: int = 0
    status: Counter = field(default_factory=Counter)

    def as_dict(self) -> dict:
        return {
            "requests": self.requests,
            "robots_requests": self.robots_requests,
            "retries": self.retries,
            "failures": self.failures,
            "bytes_received": self.bytes_received,
            "status": {str(code): n for code, n in sorted(self.status.items())},
        }


def looks_blocked(response: httpx.Response) -> bool:
    """True when a 403/429/503 carries a challenge page instead of a plain error."""
    if response.status_code not in (403, 429, 503):
        return False
    body = response.text[:8000].lower()
    return any(marker in body for marker in _BLOCK_MARKERS)


def retry_delay(attempt: int, response: httpx.Response | None, base: float = 0.5, cap: float = 60.0) -> float:
    """Seconds to wait before retry number ``attempt`` (0-based).

    ``Retry-After`` (seconds or HTTP date) wins; otherwise exponential backoff with equal jitter,
    so parallel workers that failed together do not retry together.
    """
    if response is not None and (header := response.headers.get("retry-after")):
        try:
            return min(cap, max(0.0, float(header)))
        except ValueError:
            try:
                return min(cap, max(0.0, parsedate_to_datetime(header).timestamp() - time.time()))
            except (TypeError, ValueError):
                pass
    ceiling = min(cap, base * 2**attempt)
    return ceiling / 2 + random.uniform(0, ceiling / 2)


class Fetcher:
    """Async HTTP client with robots.txt, per-host pacing, retries and block detection.

    Use it as an async context manager::

        async with Fetcher(concurrency=8, rate=8) as fetcher:
            html = await fetcher.get_text("https://books.toscrape.com/")
    """

    def __init__(
        self,
        *,
        concurrency: int = 8,
        rate: float = 8.0,
        max_retries: int = 4,
        timeout: float = 30.0,
        respect_robots: bool = True,
        user_agent: str = DEFAULT_USER_AGENT,
        proxy: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        """``rate`` is the maximum requests per second per host (Crawl-delay can only lower it).

        ``proxy`` defaults to the ``WDK_PROXY`` environment variable. ``transport`` and ``sleep``
        exist so tests can run without network and without waiting.
        """
        self.max_retries = max_retries
        self.respect_robots = respect_robots
        self.user_agent = user_agent
        self.stats = FetchStats()
        self._min_interval = 1.0 / rate if rate > 0 else 0.0
        self._sem = asyncio.Semaphore(concurrency)
        self._next_slot: dict[str, float] = {}
        self._robots: dict[str, RobotFileParser] = {}
        self._robots_lock = asyncio.Lock()
        self._blocked_hosts: set[str] = set()
        self._sleep = sleep
        client_kwargs: dict = {
            "headers": {"User-Agent": user_agent, "Accept-Language": "en;q=0.9, es;q=0.8"},
            "timeout": timeout,
            "follow_redirects": True,
        }
        if transport is not None:
            client_kwargs["transport"] = transport
        elif proxy or os.getenv("WDK_PROXY"):
            client_kwargs["proxy"] = proxy or os.getenv("WDK_PROXY")
        self._client = httpx.AsyncClient(**client_kwargs)

    async def __aenter__(self) -> Fetcher:
        return self

    async def __aexit__(self, *exc_info) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    # -- robots.txt -------------------------------------------------------------------------

    async def _robots_for(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        async with self._robots_lock:
            if origin not in self._robots:
                self._robots[origin] = await self._load_robots(origin)
            return self._robots[origin]

    async def _load_robots(self, origin: str) -> RobotFileParser:
        parser = RobotFileParser(origin + "/robots.txt")
        for attempt in range(3):
            response = None
            try:
                self.stats.robots_requests += 1
                response = await self._client.get(origin + "/robots.txt")
            except httpx.TransportError as exc:
                log.warning("robots.txt for %s unreachable: %s", origin, exc)
            if response is not None and response.status_code < 500:
                if response.status_code >= 400:
                    parser.allow_all = True
                else:
                    parser.parse(response.text.splitlines())
                return parser
            await self._sleep(retry_delay(attempt, response))
        log.error("robots.txt for %s keeps failing; treating the whole host as disallowed", origin)
        parser.disallow_all = True
        return parser

    async def check_allowed(self, url: str) -> float:
        """Raise RobotsDisallowed if robots.txt forbids ``url``; return the pacing interval for its host.

        Browser-driven code calls this before navigating, so both paths follow the same rules.
        """
        if not self.respect_robots:
            return self._min_interval
        robots = await self._robots_for(url)
        if not robots.can_fetch(self.user_agent, url):
            raise RobotsDisallowed(f"robots.txt disallows {url}")
        crawl_delay = robots.crawl_delay(self.user_agent)
        return max(self._min_interval, float(crawl_delay or 0))

    # -- pacing -----------------------------------------------------------------------------

    async def _wait_turn(self, host: str, interval: float) -> None:
        """Reserve the next free slot for ``host``. No await between read and write, so it is atomic."""
        now = time.monotonic()
        slot = max(now, self._next_slot.get(host, 0.0))
        self._next_slot[host] = slot + interval
        if slot > now:
            await self._sleep(slot - now)

    # -- requests ---------------------------------------------------------------------------

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        host = urlsplit(url).netloc
        if host in self._blocked_hosts:
            raise Blocked(f"{host} showed a challenge page earlier in this run; not requesting {url}", 403)
        interval = await self.check_allowed(url)
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            response = None
            async with self._sem:
                await self._wait_turn(host, interval)
                self.stats.requests += 1
                try:
                    response = await self._client.request(method, url, **kwargs)
                except httpx.TransportError as exc:
                    last_error = exc
            if response is not None:
                self.stats.status[response.status_code] += 1
                self.stats.bytes_received += len(response.content)
                if looks_blocked(response):
                    self.stats.failures += 1
                    self._blocked_hosts.add(host)
                    raise Blocked(
                        f"{url} answered {response.status_code} with a challenge page", response.status_code
                    )
                if response.status_code not in RETRYABLE_STATUS:
                    if response.is_error:
                        self.stats.failures += 1
                        raise FetchError(f"{method} {url} -> {response.status_code}", response.status_code)
                    return response
                last_error = FetchError(f"{method} {url} -> {response.status_code}", response.status_code)
            if attempt < self.max_retries:
                delay = retry_delay(attempt, response)
                self.stats.retries += 1
                log.warning("retry %d/%d in %.1fs: %s", attempt + 1, self.max_retries, delay, last_error)
                await self._sleep(delay)
        self.stats.failures += 1
        status = last_error.status if isinstance(last_error, FetchError) else None
        raise FetchError(f"{method} {url} failed after {self.max_retries + 1} attempts: {last_error}", status)

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("POST", url, **kwargs)

    async def get_text(self, url: str, **kwargs) -> str:
        return (await self.get(url, **kwargs)).text

    async def get_json(self, url: str, **kwargs):
        return (await self.get(url, **kwargs)).json()
