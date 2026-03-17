from datetime import datetime
import time

from src.pages.base_page import BasePage
from src.selectors.registration_selectors import *
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class RegistrationPage(BasePage):
    def open_form(self) -> None:
        self.page.locator(BUTTON_DAFTAR_BARU).first.click()
        self.page.wait_for_selector(INPUT_NIK, timeout=5000)

    def fill_nik(self, nik: str) -> None:
        self.fill(INPUT_NIK, nik)

    def fill_nama(self, nama: str) -> None:
        self.fill(INPUT_NAMA, nama)

    def fill_wa(self, nomor: str) -> None:
        self.fill(INPUT_WA, nomor)

    def fill_detail_alamat(self, alamat: str) -> None:
        self.fill(TEXTAREA_DETAIL_DOMISILI, alamat)

    def submit_step1(self) -> None:
        self.click(BUTTON_SELanjutnya)
        # tunggu kemungkinan muncul modal kuota habis
        self.page.wait_for_timeout(1000)

        try:
            if self.page.locator(MODAL_KUOTA_HABIS).is_visible():
                print("⚠ Kuota pemeriksaan hari ini habis, klik Lanjut")

                tombol_lanjut = self.page.locator(BUTTON_LANJUT_KUOTA).first
                tombol_lanjut.scroll_into_view_if_needed()
                tombol_lanjut.click(force=True)

        except Exception as e:
            print(f"⚠ Handler kuota habis tidak dijalankan: {e}")

    def continue_after_valid_modal(self) -> None:
        self.page.wait_for_selector(MODAL_DATA_VALID, timeout=10000)
        self.page.locator(BUTTON_LANJUTKAN_VALID).click()
        time.sleep(2)

    def submit_step2(self) -> None:
        self.click(BUTTON_SELanjutnya)

    def finalize_registration(self, tanggal_lahir: datetime) -> None:
        self.click(BUTTON_PILIH)
        self.click(BUTTON_DAFTARKAN_NIK)
        # self.skip_guardian_if_needed(tanggal_lahir)
        # self.click(BUTTON_DAFTAR)

        return self.handle_registration_result()

    def handle_1st_step_result(self) -> str:
        try:
            self.page.wait_for_selector(BUTTON_LANJUTKAN_VALID, timeout=10000)

            tombol_lanjutkan = self.page.locator(BUTTON_LANJUTKAN_VALID).first
            if tombol_lanjutkan.is_visible():
                print("✅ Data peserta valid, klik Lanjutkan ke step 2")
                tombol_lanjutkan.click()
                time.sleep(2)
                return "valid"

            return "unknown"

        except PlaywrightTimeoutError:
            if self.page.locator("text=Data peserta tidak valid").is_visible():
                print("⚠ Gagal submit step 1: Data peserta tidak valid")
                self.page.click("div.tracking-wide >> text='Periksa Kembali'", force=True)
                self.page.click(BUTTON_CLOSE_FORM, force=True)
                return "data_invalid"

            elif self.page.locator("text=Terjadi kesalahan").is_visible():
                print("⚠ Gagal submit step 1: Terjadi kesalahan")
                self.page.click("button.btn-fill-warning", force=True)
                self.page.click(BUTTON_CLOSE_FORM, force=True)
                return "error"

            print("❓ Tidak ada modal validasi atau error yang dikenali")
            return "unknown"

    def handle_registration_result(self) -> str:
        try:
            self.page.wait_for_selector("button.w-fill >> text=Tutup", timeout=10000)
            tombol_tutup = self.page.locator("button.w-fill >> text=Tutup")

            if tombol_tutup.is_visible():
                tombol_tutup.click()
                return "success"

            raise Exception("Tombol 'Tutup' tidak ada")

        except Exception as e:
            print(f"⚠ Tidak menemukan tombol 'Tutup': {e}")

            if self.page.locator("text=Terjadi kesalahan").is_visible():
                print("⚠ Gagal submit: Terjadi kesalahan")
                self.page.click("button.btn-fill-warning")
                self._close_registration_form()
                return "error"

            elif self.page.locator("text=Peserta Menerima Pemeriksaan").is_visible():
                print("⚠ Gagal submit: Peserta Menerima Pemeriksaan")
                self.page.click("button.btn-fill-primary:has-text('Kembali')", force=True)
                self._close_registration_form()
                return "already_examined"

            elif self.page.locator("text=Data belum sesuai KTP").is_visible():
                print("⚠ Gagal submit: Data belum sesuai KTP")
                self.page.click("button.btn-fill-primary:has-text('Perbaiki data')", force=True)
                self._close_registration_form()
                return "invalid_ktp"

            else:
                print("❓ Tidak ada tombol 'Tutup' atau modal error lainnya")
                return "unknown"
    
    def _close_registration_form(self) -> None:
        try:
            self.page.wait_for_selector(MODAL_FORM_PENDAFTARAN, timeout=5000)
            self.page.locator("button.absolute.right-4.top-3").click()
        except PlaywrightTimeoutError:
            print("⚠ Formulir pendaftaran tidak ditemukan saat akan ditutup")

    def close_success_modal(self) -> None:
        self.page.wait_for_selector("button.w-fill >> text=Tutup", timeout=10000)
        self.page.locator("button.w-fill >> text=Tutup").click()

    def select_gender(self, kode_kelamin: str | int) -> None:
        self.click("text='Pilih jenis kelamin'")
        self.page.wait_for_selector("div.cursor-pointer >> text=Laki-laki")
        if kode_kelamin in (1, "L", "l", "Laki-Laki", "Laki-laki"):
            self.click("div.cursor-pointer >> text=Laki-laki")
        elif kode_kelamin in (2, "P", "p", "Perempuan"):
            self.click("div.cursor-pointer >> text=Perempuan")

    def select_pekerjaan(self, jenis_kelamin: str) -> None:
        self.click("text='Pilih pekerjaan'")
        self.page.wait_for_selector("div.modal-content", state="visible")
        pekerjaan = "Wirausaha/Pekerja Mandiri" if str(jenis_kelamin).lower() in ["l", "laki-laki"] else "Ibu Rumah Tangga"
        self.page.get_by_text(pekerjaan, exact=True).click()

    def select_alamat(self, provinsi: str, kabupaten: str, kecamatan: str, kelurahan: str) -> None:
        self.click("text='Pilih alamat domisili'")
        self.page.wait_for_selector("div.modal-content", state="visible")
        self.page.get_by_text(provinsi, exact=True).click()
        self.page.wait_for_selector("text='Daftar Kabupaten/Kota'")
        self.page.get_by_text(kabupaten, exact=True).click()
        self.page.wait_for_selector("text='Daftar Kecamatan'")
        self.page.get_by_text(kecamatan, exact=True).click()
        self.page.wait_for_selector("text='Daftar Kelurahan'")
        self.page.get_by_text(kelurahan if kelurahan.lower() != "juntinyuat" else "Juntunyuat", exact=True).click()

    def select_birth_date(self, tanggal: datetime) -> None:
        tahun = tanggal.year
        bulan_angka = tanggal.month
        hari = tanggal.day

        trigger = self.page.locator("text='Pilih tanggal lahir'")
        if trigger.count() > 0:
            trigger.first.click()
        else:
            self.page.locator("div.mx-datepicker").nth(1).click()

        self.page.wait_for_selector("div.mx-calendar-panel-date", state="visible", timeout=5000)

        try:
            self.page.locator("button.mx-btn-current-year").first.click(timeout=5000)
        except PlaywrightTimeoutError:
            print("⚠️ Tidak bisa klik tombol tahun, coba ulang...")
            if trigger.count() > 0:
                trigger.first.click()
            else:
                self.page.locator("div.mx-datepicker").nth(1).click()
            self.page.wait_for_selector("button.mx-btn-current-year", state="visible", timeout=5000)
            self.page.locator("button.mx-btn-current-year").first.click()

        self.page.wait_for_selector("td.cell[data-year]", state="visible", timeout=5000)

        while True:
            start_year_text = self.page.inner_text(".mx-calendar-header-label span:nth-child(1)").strip()
            end_year_text = self.page.inner_text(".mx-calendar-header-label span:nth-child(3)").strip()
            start_year = int(start_year_text)
            end_year = int(end_year_text)

            if tahun < start_year:
                self.page.click(".mx-icon-double-left")
                self.page.wait_for_timeout(150)
            elif tahun > end_year:
                self.page.click(".mx-icon-double-right")
                self.page.wait_for_timeout(150)
            else:
                break

        self.page.locator(f"td.cell[data-year='{tahun}']").first.click()

        data_month = bulan_angka - 1
        self.page.wait_for_selector("td.cell[data-month]", state="visible", timeout=5000)
        self.page.locator(f"td.cell[data-month='{data_month}']").first.click()

        tanggal_str = tanggal.strftime("%Y-%m-%d")
        tanggal_print = tanggal.strftime("%d/%m/%Y")
        self.page.wait_for_selector(f"td.cell[title='{tanggal_str}']", state="visible", timeout=5000)
        self.page.locator(f"td.cell[title='{tanggal_str}']").first.click()
        print(f"✅ Tanggal lahir dipilih: {tanggal_print} (hari={hari})")

    def select_exam_date(self, total_existing: int) -> None:
        self.page.wait_for_selector("div.grid.grid-cols-7", state="visible")
        tanggal_buttons = self.page.locator("button.relative.h-auto")
        today = datetime.today().day
        for i in range(tanggal_buttons.count()):
            button = tanggal_buttons.nth(i)
            classes = button.get_attribute("class") or ""
            if "cursor-not-allowed" in classes:
                continue
            tanggal_text = button.locator("span.font-bold").text_content().strip()
            if not tanggal_text.isdigit():
                continue
            tanggal = int(tanggal_text)
            if tanggal < today:
                continue
            if tanggal == today and total_existing >= 100:
                continue
            button.click()
            return
        raise RuntimeError("Tidak ada tanggal pemeriksaan yang tersedia")
    
    def _get_age_in_days(self, tanggal_lahir: datetime) -> int:
        return (datetime.today().date() - tanggal_lahir.date()).days
    
    def _get_age_in_years(self, tanggal_lahir: datetime) -> int:
        today = datetime.today().date()
        birth = tanggal_lahir.date()
        years = today.year - birth.year
        if (today.month, today.day) < (birth.month, birth.day):
            years -= 1
        return years
    
    def needs_guardian_skip(self, tanggal_lahir: datetime) -> bool:
        """
        True jika pasien termasuk:
        - BBL   : 0-28 hari
        - Balita: < 5 tahun
        - Lansia: >= 60 tahun
        """
        age_days = self._get_age_in_days(tanggal_lahir)
        age_years = self._get_age_in_years(tanggal_lahir)

        is_bbl = 0 <= age_days <= 28
        is_balita = age_years < 5
        is_lansia = age_years >= 60

        return is_bbl or is_balita or is_lansia
    
    def skip_guardian_if_needed(self, tanggal_lahir: datetime) -> None:
        """
        Checkbox 'Daftarkan tanpa data wali' hanya dicentang bila:
        1. umur pasien masuk kategori BBL/balita/lansia
        2. checkbox memang muncul di form
        """
        if not self.needs_guardian_skip(tanggal_lahir):
            return

        self.page.wait_for_timeout(800)

        checkbox = self.page.locator("input#noWali").first
        if checkbox.count() > 0:
            try:
                checkbox.click(force=True, timeout=2000)
                self.page.wait_for_timeout(300)
                print("after input.click:", checkbox.is_checked())
                if checkbox.is_checked():
                    return True
            except Exception as e:
                print("input.click error:", e)

    def debug_guardian_section(self) -> None:
        title = self.page.locator("div.text-\\[20px\\].font-bold", has_text="Isi Data Wali")
        checkbox = self.page.locator("input#noWali")

        print("=== DEBUG DATA WALI ===")
        print(f"Title count      : {title.count()}")
        print(f"Title visible    : {title.first.is_visible() if title.count() > 0 else False}")
        print(f"Checkbox count   : {checkbox.count()}")
        print(f"Checkbox visible : {checkbox.first.is_visible() if checkbox.count() > 0 else False}")

        if title.count() > 0:
            print("Text title       :", title.first.text_content())

        if checkbox.count() > 0:
            print("Checkbox checked :", checkbox.first.is_checked())

    def debug_checkbox_no_wali(self):
        cb = self.page.locator("input#noWali").first
        print("exists   :", cb.count() > 0)
        print("visible  :", cb.is_visible() if cb.count() else False)
        print("enabled  :", cb.is_enabled() if cb.count() else False)
        print("checked  :", cb.is_checked() if cb.count() else False)
        print("box      :", cb.bounding_box() if cb.count() else None)
    
    def try_check_no_wali(self):
        checkbox = self.page.locator("input#noWali").first

        print("=== TRY CHECK NO WALI ===")
        print("before checked:", checkbox.is_checked())

        # 1. klik input langsung
        try:
            checkbox.click(force=True, timeout=2000)
            self.page.wait_for_timeout(300)
            print("after input.click:", checkbox.is_checked())
            if checkbox.is_checked():
                return True
        except Exception as e:
            print("input.click error:", e)

        # 2. pakai check()
        try:
            checkbox.check(force=True, timeout=2000)
            self.page.wait_for_timeout(300)
            print("after input.check:", checkbox.is_checked())
            if checkbox.is_checked():
                return True
        except Exception as e:
            print("input.check error:", e)

        # 3. klik teks label
        try:
            self.page.get_by_text("Daftarkan tanpa data wali", exact=True).click(timeout=2000)
            self.page.wait_for_timeout(300)
            print("after label click:", checkbox.is_checked())
            if checkbox.is_checked():
                return True
        except Exception as e:
            print("label click error:", e)

        # 4. klik parent terdekat
        try:
            checkbox.locator("xpath=..").click(force=True, timeout=2000)
            self.page.wait_for_timeout(300)
            print("after parent click:", checkbox.is_checked())
            if checkbox.is_checked():
                return True
        except Exception as e:
            print("parent click error:", e)

        # 5. pakai javascript + event
        try:
            checkbox.evaluate("""
                el => {
                    el.checked = true;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                }
            """)
            self.page.wait_for_timeout(300)
            print("after js set:", checkbox.is_checked())
            if checkbox.is_checked():
                return True
        except Exception as e:
            print("js set error:", e)

        return False

        success = self.try_check_no_wali()
        print("Final checkbox state after all attempts:", success)