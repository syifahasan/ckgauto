from datetime import datetime
from pathlib import Path

import pandas as pd

from config.settings import settings
from src.models.registration_result import RegistrationResult
from src.pages.dashboard_page import DashboardPage
from src.services.registration_service import RegistrationService
from src.readers.excel_mapper import map_row_to_patient


class RegistrationWorkflow:
    def __init__(self, page, logger, dataframe):
        self.page = page
        self.logger = logger
        self.dataframe = dataframe
        self.dashboard = DashboardPage(page)
        self.service = RegistrationService(page, logger)
        self.failed_rows = []

    def _add_failed_row(self, index, patient, reason: str, row) -> None:
        row_data = row.to_dict()
        row_data["_row_index"] = index
        row_data["_nik"] = patient.nik if patient else ""
        row_data["_nama"] = patient.nama if patient else ""
        row_data["_reason"] = reason
        self.failed_rows.append(row_data)

    def _export_failed_rows(self) -> None:
        if not self.failed_rows:
            return

        output_dir = Path(settings.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"registration_failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_path = output_dir / filename

        df_failed = pd.DataFrame(self.failed_rows)
        df_failed.to_excel(output_path, index=False)

        self.logger.info("File failed disimpan: %s", output_path)

    def run(self) -> RegistrationResult:
        result = RegistrationResult(total_rows=len(self.dataframe))
        self.dashboard.open_ckg_umum()
        self.page.click("text=Cari/Daftarkan Individu")

        for index, row in self.dataframe.iterrows():
            patient = None
            try:
                patient = map_row_to_patient(row)

                if not patient.nik:
                    result.skipped += 1
                    self.logger.warning("Baris %s dilewati: NIK kosong", index)
                    continue

                status = self.service.register(patient)

                if status == "success":
                    result.registered += 1
                    self.logger.info(
                        "Registrasi berhasil | row=%s | nik=%s | nama=%s",
                        index, patient.nik, patient.nama
                    )

                elif status == "data_invalid":
                    result.failed += 1
                    self.logger.error(
                        "Data invalid | row=%s | nik=%s | nama=%s",
                        index, patient.nik, patient.nama
                    )
                    self._add_failed_row(index, patient, "data_invalid", row)

                else:
                    result.failed += 1
                    self.logger.error(
                        "Registrasi gagal | row=%s | nik=%s | nama=%s | status=%s",
                        index, patient.nik, patient.nama, status
                    )
                    self._add_failed_row(index, patient, status or "unknown", row)

                self.page.wait_for_timeout(1000)

            except Exception as exc:
                result.failed += 1
                self.logger.exception("Gagal registrasi baris %s: %s", index, exc)
                self._add_failed_row(index, patient, str(exc), row)

                try:
                    if self.page.locator("button.absolute.right-4.top-3").count():
                        self.page.locator("button.absolute.right-4.top-3").click()
                except Exception:
                    pass

        self._export_failed_rows()
        return result