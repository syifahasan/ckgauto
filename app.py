import os
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.runners.run_confirmation import run_confirmation
from src.runners.run_registration import run_registration
from src.runners.run_service import run_service
from config.settings import settings
from src.core.browser import create_browser

DASHBOARD_SELECTOR = "section.fixed >> text='CKG Umum'"

def ensure_session(page):
    print("Membuka BASE_URL...")
    page.goto(settings.BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    print("Current URL:", page.url)

    try:
        page.wait_for_selector(DASHBOARD_SELECTOR, state="visible", timeout=8000)
        print("✅ Session masih aktif, dashboard terdeteksi.")
        return
    except PlaywrightTimeoutError:
        print("⚠ Dashboard belum terdeteksi.")
        print("⚠ Kemungkinan website redirect ke login karena session belum valid.")
        print("Silakan login manual di browser ini...")

    max_wait_ms = 180000
    interval_ms = 2000
    waited = 0

    while waited < max_wait_ms:
        print("Current URL:", page.url)

        if page.locator(DASHBOARD_SELECTOR).count() > 0 and page.locator(DASHBOARD_SELECTOR).first.is_visible():
            print("✅ Login berhasil, dashboard terdeteksi.")
            page.wait_for_timeout(5000)  # beri waktu agar session tersimpan
            return

        page.wait_for_timeout(interval_ms)
        waited += interval_ms
        print(f"Menunggu login manual... {waited // 1000} detik")

    raise RuntimeError("Timeout: dashboard tidak terdeteksi setelah menunggu login manual.")

def main():
    p, context = create_browser(settings.BROWSER_PROFILE, settings.HEADLESS)
    try:
        page = context.pages[0] if context.pages else context.new_page()
        ensure_session(page)

        mode = os.getenv("CKG_MODE", "registration").lower()
        if mode == "registration":
            run_registration(page)
        elif mode == "service":
            run_service(page)
        elif mode == "confirmation":
            run_confirmation(page)
        else:
            raise ValueError(f"Mode tidak dikenali: {mode}")
    finally:
        context.close()
        p.stop()

if __name__ == "__main__":
    main()