from src.pages.base_page import BasePage
from src.selectors.common_selectors import MENU_CKG_UMUM


class DashboardPage(BasePage):
    def open_ckg_umum(self) -> None:
        self.click(MENU_CKG_UMUM)
