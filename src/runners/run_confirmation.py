from config.settings import settings
from src.core.logger import setup_logger
from src.workflows.confirmation_workflow import ConfirmationWorkflow

def run_confirmation(page) -> None:
    logger = setup_logger(settings.LOG_DIR, name="confirmation")
    result = ConfirmationWorkflow(page, logger).run()
    logger.info("Selesai konfirmasi: %s", result)