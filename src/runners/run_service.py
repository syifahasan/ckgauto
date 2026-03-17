import os

from config.settings import settings
from src.core.logger import setup_logger
from src.readers.excel_reader import ExcelReader
from src.workflows.service_workflow import ServiceWorkflow


def run_service(page) -> None:
    logger = setup_logger(settings.LOG_DIR, name="service")

    reader = ExcelReader(settings.DATA_ILP_INPUT, sheet_name="JAN")
    start_row = int(os.getenv("CKG_START_ROW", "0"))
    start_col = int(os.getenv("CKG_START_COL", "0"))

    dataframe = reader.read(header_row=3).iloc[start_row:, start_col:].reset_index(drop=True)

    result = ServiceWorkflow(page, logger, dataframe).run()
    logger.info("Selesai pelayanan: %s", result)