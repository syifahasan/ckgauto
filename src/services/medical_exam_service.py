from src.models.service_patient import ServicePatient
from src.utils.service_normalizer import normalize_exam_values


class MedicalExamService:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

    def fill_basic_exam(self, patient: ServicePatient, jenis_kelamin: str, umur: int) -> None:
        values = normalize_exam_values(
            jk=jenis_kelamin,
            umur=umur,
            bb=patient.bb,
            tb=patient.tb,
            sistol=patient.sistol,
            diastol=patient.diastol,
            gds=patient.gds,
        )

        self._fill_nutrition(jenis_kelamin, values["bb"], values["tb"], values["lp"])
        self._fill_blood_pressure(values["sistol"], values["diastol"])
        self._fill_blood_sugar(values["gds"])

    def _find_service_row(self, keywords, exclude_keywords=None):
        if isinstance(keywords, str):
            keywords = [keywords]

        keywords = [k.lower() for k in keywords]
        exclude_keywords = [k.lower() for k in (exclude_keywords or [])]

        rows = self.page.locator("div.w-full.grid:has(button:has-text('Input Data'))")
        total = rows.count()

        print(f"DEBUG total candidate rows: {total}")

        for i in range(total):
            row = rows.nth(i)
            text = self._normalize_text(row.inner_text())

            print(f"DEBUG _find_service_row rows[{i}] text: {text}")

            if all(k in text for k in keywords) and not any(ex in text for ex in exclude_keywords):
                print(f"DEBUG matched row[{i}] for keywords={keywords}")
                return row

        return None

    def _click_input_data(self, row) -> bool:
        if row is None or row.count() == 0:
            return False

        btn = row.get_by_role("button", name="Input Data").first
        if btn.count() == 0:
            return False

        btn.scroll_into_view_if_needed()
        btn.click(force=True)
        self.page.wait_for_timeout(500)
        return True

    def _fill_nutrition(self, jk: str, bb: int, tb: int, lp: int) -> None:
        row = self._find_service_row(["gizi", jk, "bb", "tb"])

        if not row:
            self.logger.warning("Form status gizi tidak ditemukan")
            return

        self._click_input_data(row)
        self.page.fill("#sq_100i", str(bb))
        self.page.fill("#sq_101i", str(tb))
        self.page.fill("#sq_102i", str(lp))
        self._submit_exam_form()

    def _fill_blood_pressure(self, sistol: int, diastol: int) -> None:
        row = self._find_service_row(["tekanan", "darah"])

        if not row:
            self.logger.warning("Form tekanan darah tidak ditemukan")
            return

        self._click_input_data(row)
        self.page.fill("#sq_100i", str(sistol))
        self.page.fill("#sq_101i", str(diastol))
        self._submit_exam_form()

    def _fill_blood_sugar(self, gds: int) -> None:
        row = self._find_service_row(["gula", "darah"])

        if not row:
            self.logger.warning("Form gula darah sewaktu tidak ditemukan")
            return

        self._click_input_data(row)
        self.page.fill("#sq_100i", str(gds))
        self._submit_exam_form()

    def _normalize_text(self, text: str) -> str:
        return " ".join(text.lower().split())
    
    def _row_contains_all(self, row_text: str, keywords: list[str]) -> bool:
        return all(keyword.lower() in row_text for keyword in keywords)

    def _submit_exam_form(self) -> None:
        self.page.locator("input[title='Kirim']").click()

        # tunggu form/modal hilang
        self.page.wait_for_timeout(1000)

        # tunggu tabel layanan muncul lagi
        self.page.wait_for_selector("#tableLayanan", timeout=10000)
        self.page.wait_for_timeout(1000)