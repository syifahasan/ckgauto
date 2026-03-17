from src.models.confirmation_result import ConfirmationResult
from src.pages.dashboard_page import DashboardPage
from src.pages.confirmation_page import ConfirmationPage
from src.selectors.common_selectors import BUTTON_NEXT_PAGE, PAGINATION_ITEMS
from src.services.confirmation_service import ConfirmationService


class ConfirmationWorkflow:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self.dashboard = DashboardPage(page)
        self.confirmation_page = ConfirmationPage(page)
        self.service = ConfirmationService(page, logger)

    def _get_total_pages(self) -> int:
        buttons = self.page.locator(PAGINATION_ITEMS)
        last_page_text = buttons.nth(-2).inner_text()
        if last_page_text.isdigit():
            return int(last_page_text)
        texts = [b.inner_text() for b in buttons.all()]
        angka = [int(t) for t in texts if t.isdigit()]
        return max(angka) if angka else 1

    def run(self) -> ConfirmationResult:
        result = ConfirmationResult()
        self.dashboard.open_ckg_umum()
        self.confirmation_page.open_listing()
        result.total_pages = self._get_total_pages()
        for index in range(result.total_pages):
            self.logger.info("Konfirmasi halaman %s/%s", index + 1, result.total_pages)
            result.total_confirmed += self.service.process_current_page()
            if index < result.total_pages - 1:
                self.page.locator(BUTTON_NEXT_PAGE).last.click()
                self.page.wait_for_timeout(1500)
        return result
