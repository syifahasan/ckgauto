import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from playwright.sync_api import sync_playwright


BASE_URL = "https://sehatindonesiaku.kemkes.go.id/"
SESSION_FILE = "data/session/auth.json"


def save_session():
    os.makedirs("data/session", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        context = browser.new_context()
        page = context.new_page()

        page.goto(BASE_URL)

        print("Silakan login manual terlebih dahulu, termasuk captcha.")
        input("Setelah berhasil login dan sudah masuk dashboard, tekan Enter di terminal...")

        context.storage_state(path=SESSION_FILE)
        print(f"Session berhasil disimpan ke: {SESSION_FILE}")

        browser.close()


if __name__ == "__main__":
    save_session()