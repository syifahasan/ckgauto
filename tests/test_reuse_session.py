import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.core.browser import create_browser

BASE_URL = "https://your-url-login"
PROFILE_PATH = os.path.join(ROOT_DIR, "data", "profile", "ckg")


def test_reuse_session():
    p, context = create_browser(profile_path=PROFILE_PATH, headless=False)

    try:
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_timeout(5000)

        print("URL sekarang:", page.url)

        if "login" in page.url.lower():
            print("Session tidak aktif, login manual lagi.")
        else:
            print("Session aktif, tidak perlu login ulang.")

        input("Tekan Enter untuk selesai...")

    finally:
        context.close()
        p.stop()


if __name__ == "__main__":
    test_reuse_session()