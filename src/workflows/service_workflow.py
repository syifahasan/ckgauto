from src.models.service_result import ServiceResult
from src.pages.dashboard_page import DashboardPage
from src.pages.service_page import ServicePage
from src.services.medical_exam_service import MedicalExamService
from src.services.screening_service import ScreeningService
from src.readers.service_excel_mapper import map_row_to_service_patient
from datetime import datetime


class ServiceWorkflow:
    def __init__(self, page, logger, dataframe):
        self.page = page
        self.logger = logger
        self.dataframe = dataframe
        self.dashboard = DashboardPage(page)
        self.service_page = ServicePage(page)
        self.exam_service = MedicalExamService(page, logger)
        self.screening_service = ScreeningService(page, logger)

    def run(self) -> ServiceResult:
        result = ServiceResult(total_pages=1)

        self.dashboard.open_ckg_umum()
        self.service_page.open_service_menu()
        self.service_page.save_modal_if_present()
        self.service_page.choose_date(datetime(2026, 3, 16))
        

        for index, row in self.dataframe.iterrows():
            try:
                patient = map_row_to_service_patient(row)

                if not patient.nik:
                    result.total_failed += 1
                    self.logger.warning("Baris %s dilewati: NIK kosong", index)
                    continue

                started = self.service_page.click_start_by_nik(patient.nik)
                self.page.wait_for_load_state("networkidle")
                if not started:
                    result.total_failed += 1
                    self.logger.warning("NIK %s tidak ditemukan / tidak bisa mulai pelayanan", patient.nik)
                    continue

                jk, umur = self.service_page.extract_patient_context()

                # self.screening_service.fill_mandatory_screening(jk, umur)

                if self.page.locator("button:has(div.tracking-wide:has-text('Mulai Pemeriksaan'))").count():
                    self.page.locator("button:has(div.tracking-wide:has-text('Mulai Pemeriksaan'))").click()

                self.exam_service.fill_basic_exam(patient, jk, umur)

                result.total_started += 1
                result.total_completed += 1
                self.logger.info("Pelayanan berhasil untuk NIK=%s | nama=%s", patient.nik, patient.nama)

            except Exception as exc:
                result.total_failed += 1
                self.logger.exception("Gagal memproses pelayanan baris %s: %s", index, exc)

                try:
                    if self.page.locator("button.absolute.right-4.top-3").count():
                        self.page.locator("button.absolute.right-4.top-3").click()
                except Exception:
                    pass

        return result