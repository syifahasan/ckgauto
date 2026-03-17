import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.core.browser import create_browser

BASE_URL = "https://your-url-login"
PROFILE_PATH = os.path.join(ROOT_DIR, "data", "profile", "ckg")


def test_manual_login():
    os.makedirs(PROFILE_PATH, exist_ok=True)

    p, context = create_browser(profile_path=PROFILE_PATH, headless=False)

    try:
        page = context.new_page()
        page.goto(BASE_URL)

        print("Silakan login manual terlebih dahulu.")
        print("Setelah login berhasil dan captcha selesai, tekan Enter.")
        input()

    finally:
        context.close()
        p.stop()


if __name__ == "__main__":
    test_manual_login()