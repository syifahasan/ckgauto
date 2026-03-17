class ScreeningService:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

    def fill_mandatory_screening(self, jenis_kelamin: str, umur: int) -> None:
        """Starter refactor untuk skrining mandiri.

        Saat ini baru berfungsi sebagai titik ekstensi. Rule-rule dari `pelayananumum.py`
        bisa dipindahkan bertahap ke method-method terpisah seperti:
        - fill_mental_health()
        - fill_smoking_behavior()
        - fill_physical_activity()
        - fill_lung_cancer_risk()
        - fill_colon_cancer_risk()
        """
        self.logger.info(
            "Screening placeholder dipanggil | jenis_kelamin=%s | umur=%s",
            jenis_kelamin,
            umur,
        )
