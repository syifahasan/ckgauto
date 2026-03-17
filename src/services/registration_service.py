import re

from config.constants import DEFAULT_CITY, DEFAULT_DISTRICT, DEFAULT_PHONE, DEFAULT_PROVINCE
from src.models.patient import Patient
from src.pages.registration_page import RegistrationPage
from src.utils.phone_utils import normalize_phone_number


class RegistrationService:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self.registration_page = RegistrationPage(page)

    def get_total_existing(self) -> int:
        blok = self.page.locator("div:has-text('Menampilkan')")
        b_items = blok.locator("b")
        if b_items.count() < 2:
            return 0
        total_text = b_items.nth(1).text_content().strip()
        match = re.search(r"(\d+)", total_text)
        print(f"DEBUG total_existing = {total_text}")
        return int(match.group(1)) if match else 0

    def register(self, patient: Patient) -> str:
        self.registration_page.open_form()
        if not patient.nik:
            raise ValueError("NIK kosong")

        self.registration_page.fill_nik(patient.nik)
        self.registration_page.fill_nama(patient.nama)
        self.registration_page.select_birth_date(patient.tanggal_lahir)
        self.registration_page.skip_guardian_if_needed(patient.tanggal_lahir)
        self.registration_page.select_gender(patient.jenis_kelamin)
        self.registration_page.fill_wa(normalize_phone_number(patient.no_wa or DEFAULT_PHONE))
        self.registration_page.select_exam_date(self.get_total_existing())

        self.registration_page.submit_step1()
        step1_result = self.registration_page.handle_1st_step_result()
        print(f"DEBUG step1_result = {step1_result!r}")

        if step1_result != "valid":
            return step1_result

        self.registration_page.select_pekerjaan(patient.jenis_kelamin)
        self.registration_page.select_alamat(
            DEFAULT_PROVINCE,
            DEFAULT_CITY,
            DEFAULT_DISTRICT,
            patient.kelurahan
        )
        self.registration_page.fill_detail_alamat(patient.alamat_detail or patient.kelurahan)
        self.registration_page.submit_step2()

        final_result = self.registration_page.finalize_registration(patient.tanggal_lahir)
        return final_result or "unknown"