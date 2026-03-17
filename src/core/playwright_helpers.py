from playwright.sync_api import Page


def safe_click(page: Page, selector: str, timeout: int = 5000) -> None:
    page.locator(selector).first.click(timeout=timeout)


def safe_fill(page: Page, selector: str, value: str, timeout: int = 5000) -> None:
    page.locator(selector).first.fill(value, timeout=timeout)


def text_content(page: Page, selector: str, default: str = "") -> str:
    locator = page.locator(selector).first
    return locator.text_content().strip() if locator.count() else default
