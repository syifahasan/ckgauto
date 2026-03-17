import re
from datetime import datetime
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.pages.base_page import BasePage
from src.selectors.service_selectors import *


class ServicePage(BasePage):
    # selector lokal agar tidak wajib ubah service_selectors.py
    SEARCH_METHOD_DROPDOWN = "div.border.border-b-2.border-b-solid.border-gray-200.flex"
    SEARCH_OPTION_NIK = "div.cursor-pointer.px-3:has-text('NIK')"
    SEARCH_INPUT = "input[placeholder*='Masukkan']"
    TABLE_ROWS = "div.overflow-auto.table-individu-terdaftar table tbody tr"

    TAB_BELUM = "div.cursor-pointer.px-3:has-text('Belum Pemeriksaan')"
    TAB_SEDANG = "div.cursor-pointer.px-3:has-text('Sedang Pemeriksaan')"

    def open_service_menu(self) -> None:
        self.click(MENU_PELAYANAN)
        self.page.wait_for_load_state("networkidle")

    def choose_date(self, tanggal: datetime | None = None) -> None:
        """
        Pilih tanggal pada date picker.

        Args:
            tanggal (datetime | None): tanggal yang ingin dipilih.
            Jika None maka otomatis memilih tanggal hari ini.
        """

        if tanggal is None:
            tanggal = datetime.today()

        self.click(DATE_PICKER_TRIGGER)

        tanggal_str = tanggal.strftime("%Y-%m-%d")
        selector_tanggal = f"td.cell[title='{tanggal_str}']"

        cell = self.page.locator(selector_tanggal).first
        cell.click()
        self.page.wait_for_timeout(200)
        cell.click()

    def choose_today(self) -> None:
        self.click(DATE_PICKER_TRIGGER)
        tanggal_str = datetime.today().strftime("%Y-%m-%d")
        selector_tanggal = f"td.cell[title='{tanggal_str}']"
        self.page.locator(selector_tanggal).first.click()
        self.page.wait_for_timeout(200)
        self.page.locator(selector_tanggal).first.click()

    def save_modal_if_present(self) -> None:
        try:
            time.sleep(2)
            modal = self.page.locator("text=Pengaturan Pelayanan")
            modal.wait_for(state="visible", timeout=3000)

            checkbox_input = self.page.locator("input#sameLocation").first
            checkbox_ui = self.page.locator("input#sameLocation + div.check").first

            if checkbox_input.count() and not checkbox_input.is_checked():
                try:
                    checkbox_input.set_checked(True, timeout=2000)
                except Exception:
                    checkbox_ui.click(force=True, timeout=2000)

            self.page.get_by_role("button", name="Simpan").click()
        except PlaywrightTimeoutError:
            pass

    def search_patient_by_nik(self, nik: str) -> str | None:
        """
        Cari pasien berdasarkan NIK.
        Prioritas:
        1. Belum Pemeriksaan
        2. Sedang Pemeriksaan

        Return:
            - "belum" jika ditemukan di tab Belum
            - "sedang" jika ditemukan di tab Sedang
            - None jika tidak ditemukan
        """
        self._select_search_method_nik()
        self._fill_search_keyword(nik)
        # Cari di tab Belum
        self._open_tab_belum()
        print("TAB aktif setelah klik Belum:", self.page.locator("text=Belum Pemeriksaan").first.inner_text())
        
        print("Belum rows:", self.page.locator("table tbody tr").count())
        if self._has_search_result():
            return "belum"

        # Cari di tab Sedang
        self._open_tab_sedang()
        # self._fill_search_keyword(nik)
        print("Sedang rows:", self.page.locator("table tbody tr").count())
        if self._has_search_result():
            return "sedang"

        return None

    def click_start_first_result(self) -> bool:
        rows = self.page.locator(self.TABLE_ROWS)
        total_rows = rows.count()

        print("DEBUG click_start_first_result rows:", total_rows)

        for i in range(total_rows):
            row = rows.nth(i)
            btn = row.locator("button:has(div.tracking-wide:has-text('Mulai'))")

            if btn.count() > 0 and btn.first.is_visible():
                btn.first.scroll_into_view_if_needed()
                btn.first.click(force=True)
                self.page.wait_for_timeout(1000)
                return True

        return False

    def click_start_by_nik(self, nik: str) -> bool:
        found_in = self.search_patient_by_nik(nik)
        if not found_in:
            return False

        return self.click_start_first_result()

    def extract_patient_context(self) -> tuple[str, int]:
        jenis_kelamin = self.page.locator(
            "//div[contains(text(), 'Jenis Kelamin')]/following-sibling::div"
        ).inner_text()

        umur_raw = self.page.locator(
            "//div[contains(text(), 'Umur')]/following-sibling::div"
        ).inner_text()

        match = re.search(r"(\d+)\s*Tahun", umur_raw)
        umur = int(match.group(1)) if match else 0

        return jenis_kelamin, umur

    # =========================
    # PRIVATE HELPERS
    # =========================

    def _select_search_method_nik(self) -> None:
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

        trigger = self.page.locator("div.cursor-pointer:has(span:text-is('Nama'))").first
        if trigger.count() == 0:
            trigger = self.page.locator("div.cursor-pointer:has(span:text-is('NIK'))").first

        if trigger.count() == 0 or not trigger.is_visible():
            raise RuntimeError("Trigger dropdown pencarian tidak ditemukan")

        current_text = trigger.inner_text().strip()
        if current_text == "NIK":
            return

        trigger.click(force=True)
        self.page.wait_for_timeout(700)

        nik_option = self.page.locator("text=NIK").last
        if nik_option.count() == 0 or not nik_option.is_visible():
            raise RuntimeError("Opsi NIK tidak muncul setelah dropdown dibuka")

        nik_option.click(force=True)
        self.page.wait_for_timeout(500)

    def _open_search_method_dropdown(self) -> None:
        candidates = [
            "div.cursor-pointer:has(span:text-is('Nama'))",
            "div.cursor-pointer:has(span:text-is('NIK'))",
            "span:text-is('Nama')",
            "span:text-is('NIK')",
        ]

        for selector in candidates:
            loc = self.page.locator(selector).first
            if loc.count() > 0 and loc.is_visible():
                loc.scroll_into_view_if_needed()
                self.page.wait_for_timeout(200)

                try:
                    if loc.locator("xpath=ancestor::div[contains(@class,'cursor-pointer')]").count() > 0:
                        loc.locator("xpath=ancestor::div[contains(@class,'cursor-pointer')]").first.click(force=True)
                    else:
                        loc.click(force=True)
                    self.page.wait_for_timeout(500)
                    return
                except Exception:
                    continue

        raise RuntimeError("Tidak berhasil membuka dropdown metode pencarian")

    def _fill_search_keyword(self, keyword: str) -> None:
        search_input = self.page.locator("input[placeholder*='Masukkan']").first
        search_input.click()
        search_input.fill("")
        search_input.type(str(keyword))
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(1500)

    def _open_tab_belum(self) -> None:
        self._open_tab_by_text("Belum Pemeriksaan")

    def _open_tab_sedang(self) -> None:
        self._open_tab_by_text("Sedang Pemeriksaan")

    def _open_tab_by_text(self, tab_text: str) -> None:
        tabs = self.page.locator("div.cursor-pointer.px-3")

        total = tabs.count()
        for i in range(total):
            tab = tabs.nth(i)
            try:
                if not tab.is_visible():
                    continue

                text = " ".join(tab.inner_text().split())
                if tab_text in text:
                    tab.scroll_into_view_if_needed()
                    tab.click(force=True)
                    self.page.wait_for_timeout(800)
                    return
            except Exception:
                continue

    def _has_search_result(self) -> bool:
        rows = self.page.locator("table tbody tr")
        data = rows.locator("td").filter(has_text=re.compile("Belum Pemeriksaan|Sedang Pemeriksaan"))
        total_rows = data.count()

        print("DEBUG total rows:", total_rows)

        if total_rows == 0:
            return False

        for i in range(total_rows):
            row = data.nth(i)
            text = " ".join(row.inner_text().split()).lower()
            print(f"DEBUG row[{i}] text:", text)

            if text and "tidak ada data" not in text:
                return True

        return False



    def _find_first_valid_row(self):
        rows = self.page.locator(self.TABLE_ROWS)
        total_rows = rows.count()

        if total_rows == 0:
            return None

        for i in range(total_rows):
            row = rows.nth(i)

            status_belum = row.locator("td").filter(has_text="Belum Pemeriksaan").count() > 0
            status_sedang = row.locator("td").filter(has_text="Sedang Pemeriksaan").count() > 0
            has_mulai = row.locator(BUTTON_MULAI).count() > 0

            if (status_belum or status_sedang) and has_mulai:
                return row

        return None