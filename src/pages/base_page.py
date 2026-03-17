from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, selector: str) -> None:
        self.page.locator(selector).first.click()

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).first.fill(value)

    def is_visible(self, selector: str) -> bool:
        locator = self.page.locator(selector).first
        return locator.count() > 0 and locator.is_visible()
