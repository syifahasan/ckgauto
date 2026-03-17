from playwright.sync_api import expect
from src.browser import create_browser

BASE_URL = "https://sehatindonesiaku.kemkes.go.id/"
PROFILE_PATH = r"E:\ChromeProfileAutomation"

def test_navigasi_menu():
    p, context = create_browser(PROFILE_PATH, headless=False)
    page = context.new_page()

    try:
        page.goto(BASE_URL, wait_until="networkidle")

        # Pastikan masih login
        # Ganti locator ini sesuai elemen yang muncul setelah login sukses
        expect(page.locator("text=Profil")).to_be_visible(timeout=10000)

        # Contoh navigasi ke menu Daftar Umum
        page.click("text=Daftar Umum")
        expect(page).to_have_url(lambda url: "daftar" in url)
        expect(page.locator("h1")).to_contain_text("Daftar Umum")

        # Contoh navigasi ke menu Konfirmasi Umum
        page.click("text=Konfirmasi Umum")
        expect(page).to_have_url(lambda url: "konfirmasi" in url)
        expect(page.locator("h1")).to_contain_text("Konfirmasi Umum")

    finally:
        context.close()
        p.stop()