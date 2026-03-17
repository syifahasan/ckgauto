from src.pages.confirmation_page import ConfirmationPage


class ConfirmationService:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self.confirmation_page = ConfirmationPage(page)

    def process_current_page(self) -> int:
        total = self.confirmation_page.total_pending()
        for _ in range(total):
            self.confirmation_page.confirm_first()
        self.logger.info("Halaman selesai. total_confirmed=%s", total)
        return total
