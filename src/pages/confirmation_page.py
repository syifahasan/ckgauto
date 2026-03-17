from src.pages.base_page import BasePage
from src.selectors.confirmation_selectors import BUTTON_CLOSE_SUCCESS, MENU_CARI_DAFTAR, BUTTON_KONFIRMASI, CHECK_VERIFY, BUTTON_HADIR
from src.selectors.common_selectors import BUTTON_CLOSE_MODAL


class ConfirmationPage(BasePage):
    def open_listing(self) -> None:
        self.click(MENU_CARI_DAFTAR)

    def total_pending(self) -> int:
        return self.page.locator(BUTTON_KONFIRMASI).count()

    def confirm_first(self) -> None:
        self.page.locator(BUTTON_KONFIRMASI).first.click()
        self.page.wait_for_selector("div.max-h-full", timeout=5000)
        self.page.wait_for_selector("input#verify", timeout=5000)
        self.click(CHECK_VERIFY)
        self.page.locator(BUTTON_HADIR).last.click()
        self.page.locator(BUTTON_CLOSE_SUCCESS).click()
        if self.page.locator(BUTTON_CLOSE_MODAL).count():
            self.click(BUTTON_CLOSE_MODAL)
