import os

from config.settings import settings
from src.core.logger import setup_logger
from src.readers.excel_reader import ExcelReader
from src.workflows.registration_workflow import RegistrationWorkflow

def run_registration(page) -> None:
    logger = setup_logger(settings.LOG_DIR, name="registration")
    reader = ExcelReader(settings.INPUT_EXCEL)
    start_row = int(os.getenv("CKG_START_ROW", "0"))
    start_col = int(os.getenv("CKG_START_COL", "0"))
    dataframe = reader.read_slice(start_row=start_row, start_col=start_col)

    result = RegistrationWorkflow(page, logger, dataframe).run()
    logger.info("Selesai registrasi: %s", result)