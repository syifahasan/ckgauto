from playwright.sync_api import Page


def wait_visible(page: Page, selector: str, timeout: int = 5000) -> None:
    page.wait_for_selector(selector, state="visible", timeout=timeout)


def wait_hidden(page: Page, selector: str, timeout: int = 5000) -> None:
    page.wait_for_selector(selector, state="hidden", timeout=timeout)
