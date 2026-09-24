import asyncio

import httpx
import pytest

from wdk.fetch import Blocked, Fetcher, FetchError, RobotsDisallowed, retry_delay

ROBOTS_OK = "User-agent: *\nDisallow: /private/\n"


def make_fetcher(handler, fake_sleep, **kwargs) -> Fetcher:
    return Fetcher(transport=httpx.MockTransport(handler), sleep=fake_sleep, rate=0, **kwargs)


def run(coro):
    return asyncio.run(coro)


def test_retries_transient_errors_then_succeeds(fake_sleep):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text=ROBOTS_OK)
        calls["n"] += 1
        return httpx.Response(503) if calls["n"] < 3 else httpx.Response(200, text="ok")

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            return await f.get_text("https://example.test/page"), f.stats

    text, stats = run(go())
    assert text == "ok"
    assert stats.retries == 2 and stats.failures == 0
    assert stats.status[503] == 2 and stats.status[200] == 1


def test_retry_after_header_wins(fake_sleep):
    calls = {"n": 0}

    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "7"})
        return httpx.Response(200, text="ok")

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            return await f.get_text("https://example.test/")

    assert run(go()) == "ok"
    assert 7.0 in fake_sleep.calls


def test_gives_up_after_max_retries(fake_sleep):
    def handler(request):
        return httpx.Response(404) if request.url.path == "/robots.txt" else httpx.Response(500)

    async def go():
        async with make_fetcher(handler, fake_sleep, max_retries=2) as f:
            try:
                await f.get("https://example.test/")
            finally:
                assert f.stats.failures == 1 and f.stats.retries == 2

    with pytest.raises(FetchError) as info:
        run(go())
    assert info.value.status == 500


def test_client_errors_are_not_retried(fake_sleep):
    def handler(request):
        return httpx.Response(404)

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            await f.get("https://example.test/missing")

    with pytest.raises(FetchError) as info:
        run(go())
    assert info.value.status == 404
    assert fake_sleep.calls == []


def test_robots_disallow_is_enforced(fake_sleep):
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text=ROBOTS_OK)
        raise AssertionError("a disallowed URL must never be requested")

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            await f.get("https://example.test/private/data")

    with pytest.raises(RobotsDisallowed):
        run(go())


def test_robots_5xx_means_stay_out(fake_sleep):
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(503)
        raise AssertionError("host must be treated as disallowed")

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            await f.get("https://example.test/anything")

    with pytest.raises(RobotsDisallowed):
        run(go())


def test_crawl_delay_slows_pacing(fake_sleep):
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nCrawl-delay: 2\n")
        return httpx.Response(200, text="ok")

    async def go():
        async with make_fetcher(handler, fake_sleep, concurrency=1) as f:
            for _ in range(3):
                await f.get("https://example.test/")

    run(go())
    # first request goes out immediately, the next two wait ~2 s each
    assert len(fake_sleep.calls) == 2
    assert all(1.9 < s <= 4.1 for s in fake_sleep.calls)


def test_challenge_page_stops_the_run_without_retrying(fake_sleep):
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(403, text="<html><title>Attention Required!</title>captcha</html>")

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            await f.get("https://example.test/")

    with pytest.raises(Blocked):
        run(go())
    assert fake_sleep.calls == []


def test_retry_delay_backoff_grows_and_is_capped():
    delays = [retry_delay(n, None, base=1, cap=10) for n in range(6)]
    assert 0.5 <= delays[0] <= 1
    assert 4 <= delays[3] <= 8
    assert all(d <= 10 for d in delays)


def test_after_a_challenge_the_host_is_not_contacted_again(fake_sleep):
    calls = {"n": 0}

    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        calls["n"] += 1
        return httpx.Response(403, text="captcha")

    async def go():
        async with make_fetcher(handler, fake_sleep) as f:
            for path in ("/a", "/b", "/c"):
                with pytest.raises(Blocked):
                    await f.get("https://example.test" + path)

    run(go())
    assert calls["n"] == 1
