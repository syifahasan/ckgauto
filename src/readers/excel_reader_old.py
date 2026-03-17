from pathlib import Path
import pandas as pd


class ExcelReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read(self) -> pd.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {self.file_path}")

        df = pd.read_excel(self.file_path)
        if df.empty:
            raise ValueError("File Excel kosong atau tidak ada data yang valid.")
        return df

    def read_slice(self, start_row: int = 0, start_col: int = 0) -> pd.DataFrame:
        df = self.read()
        data = df.iloc[start_row:, start_col:].reset_index(drop=True)
        if data.empty:
            raise ValueError("Slice Excel kosong. Cek start_row/start_col.")
        return data
