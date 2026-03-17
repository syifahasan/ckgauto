from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    BASE_URL: str = os.getenv("CKG_BASE_URL", "https://sehatindonesiaku.kemkes.go.id/")
    BROWSER_PROFILE: str = os.getenv("CKG_BROWSER_PROFILE", "E:/ChromeProfileAutomation")
    HEADLESS: bool = os.getenv("CKG_HEADLESS", "false").lower() == "true"
    INPUT_EXCEL: str = os.getenv("CKG_INPUT_EXCEL", "./data/input/pasien.xlsx")
    DATA_ILP_INPUT: str = os.getenv("CKG_DATA_ILP_INPUT", "./data/input/REGISTER MANUAL CKG 1.xlsx")
    OUTPUT_DIR: str = os.getenv("CKG_OUTPUT_DIR", "./data/output")
    LOG_DIR: str = os.getenv("CKG_LOG_DIR", "./data/logs")
    TIMEOUT_MS: int = int(os.getenv("CKG_TIMEOUT_MS", "10000"))
    NAVIGATION_TIMEOUT_MS: int = int(os.getenv("CKG_NAVIGATION_TIMEOUT_MS", "20000"))

    EMAIL: str = os.getenv("CKG_EMAIL", "")
    PASSWORD: str = os.getenv("CKG_PASSWORD", "")

settings = Settings()