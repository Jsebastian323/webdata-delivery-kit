"""Playwright helpers for pages that only exist after JavaScript runs.

This module is imported lazily, so static cases never pay for a browser. Before reaching for
it, check the page source and the network tab: most "JavaScript pages" ship their data as
JSON somewhere.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from playwright.async_api import Page, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeout

from .fetch import DEFAULT_USER_AGENT


@asynccontextmanager
async def open_page(*, headless: bool = True, user_agent: str = DEFAULT_USER_AGENT) -> AsyncIterator[Page]:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context(user_agent=user_agent)
        try:
            yield await context.new_page()
        finally:
            await context.close()
            await browser.close()


async def scroll_to_end(
    page: Page, item_selector: str, *, max_rounds: int = 200, patience_ms: int = 4000
) -> int:
    """Scroll an infinite list until no new items arrive; return the final item count.

    After each scroll it waits until the number of items grows, and gives up after
    ``patience_ms`` without growth: that silence is the end of the list. (Waiting for
    "networkidle" does not work here: it only describes the initial page load, so it returns
    at once and stops the scroll early.)
    """
    count = await page.locator(item_selector).count()
    for _ in range(max_rounds):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        try:
            await page.wait_for_function(
                "([selector, seen]) => document.querySelectorAll(selector).length > seen",
                arg=[item_selector, count],
                timeout=patience_ms,
            )
        except PlaywrightTimeout:
            break
        count = await page.locator(item_selector).count()
    return count
