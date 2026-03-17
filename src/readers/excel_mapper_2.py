from datetime import datetime
from typing import Any
import pandas as pd

from src.models.patient import Patient
from src.readers.validators import is_empty


def _normalize_nik(value: Any) -> str:
    if is_empty(value):
        return ""
    if isinstance(value, float):
        return str(int(value))
    return str(value).strip()


def map_row_to_patient(row: pd.Series) -> Patient:
    tanggal_lahir = pd.to_datetime(row[7])
    kelurahan = "" if is_empty(row[13]) else str(row[13]).strip().title()
    return Patient(
        nik=_normalize_nik(row[3]),
        nama=str(row[1]).strip(),
        tanggal_lahir=tanggal_lahir.to_pydatetime() if hasattr(tanggal_lahir, 'to_pydatetime') else tanggal_lahir,
        jenis_kelamin=str(row[6]).strip(),
        no_wa="",
        kelurahan=kelurahan,
        alamat_detail=kelurahan,
    )
