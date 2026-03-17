from __future__ import annotations

from typing import Any, Optional
import pandas as pd

from src.models.service_patient import ServicePatient
from src.readers.validators import is_empty, normalize_digits


COLUMN_MAP = {
    "nama": "Nama",
    "nik": "NIK",
    "bb": "BB",
    "tb": "TB",
    "tekanan_darah": "Tekanan Darah",
    "gds": "GDS",
}


def _get(row: pd.Series, column_name: str, default: Any = "") -> Any:
    return row[column_name] if column_name in row.index else default


def _to_float(value: Any) -> Optional[float]:
    if is_empty(value):
        return None
    try:
        return float(str(value).replace(",", ".").strip())
    except Exception:
        return None


def _to_int(value: Any) -> Optional[int]:
    if is_empty(value):
        return None
    try:
        return int(float(str(value).replace(",", ".").strip()))
    except Exception:
        return None


def _parse_blood_pressure(value: Any) -> tuple[Optional[int], Optional[int]]:
    """
    Mendukung format:
    - 120/80
    - 120 / 80
    - 120-80
    - 120
    """
    if is_empty(value):
        return None, None

    text = str(value).strip().replace(" ", "")
    for sep in ["/", "-", "_"]:
        if sep in text:
            parts = text.split(sep)
            if len(parts) >= 2:
                sistol = _to_int(parts[0])
                diastol = _to_int(parts[1])
                return sistol, diastol

    # fallback kalau hanya satu angka
    only_digits = normalize_digits(text)
    if only_digits:
        return _to_int(only_digits), None

    return None, None


def map_row_to_service_patient(row: pd.Series) -> ServicePatient:
    tekanan = _get(row, COLUMN_MAP["tekanan_darah"])
    sistol, diastol = _parse_blood_pressure(tekanan)

    return ServicePatient(
        nik=normalize_digits(_get(row, COLUMN_MAP["nik"])),
        nama="" if is_empty(_get(row, COLUMN_MAP["nama"])) else str(_get(row, COLUMN_MAP["nama"])).strip(),
        bb=_to_float(_get(row, COLUMN_MAP["bb"])),
        tb=_to_float(_get(row, COLUMN_MAP["tb"])),
        sistol=sistol,
        diastol=diastol,
        gds=_to_int(_get(row, COLUMN_MAP["gds"])),
    )