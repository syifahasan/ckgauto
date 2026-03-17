from __future__ import annotations

from typing import Any

import pandas as pd

from src.models.patient import Patient
from src.readers.validators import is_empty, normalize_digits, normalize_phone


COLUMN_MAP = {
    "nama": "Nama Pasien",
    "no_rm": "No. eRM",
    "nik": "NIK",
    "jenis_kelamin": "Jenis Kelamin",
    "tanggal_lahir": "Tgl.Lahir",
    "kelurahan": "Kelurahan",
    "alamat": "Alamat",
    "rt": "RT",
    "rw": "RW",
    "no_telp": "No Telp",
}


def _get(row: pd.Series, column_name: str, default: Any = "") -> Any:
    return row[column_name] if column_name in row.index else default


def _normalize_nik(value: Any) -> str:
    if is_empty(value):
        return ""
    return normalize_digits(value)


def _normalize_name(value: Any) -> str:
    if is_empty(value):
        return ""
    return str(value).strip()


def _normalize_kelurahan(value: Any) -> str:
    if is_empty(value):
        return ""
    return str(value).strip().title()


def _normalize_gender(value: Any) -> str:
    if is_empty(value):
        return ""
    raw = str(value).strip().lower()
    mapping = {
        "l": "Laki-laki",
        "laki-laki": "Laki-laki",
        "lakilaki": "Laki-laki",
        "p": "Perempuan",
        "perempuan": "Perempuan",
        "wanita": "Perempuan",
    }
    return mapping.get(raw, str(value).strip())


def _normalize_birth_date(value: Any):
    if is_empty(value):
        return None

    tanggal_lahir = pd.to_datetime(value, errors="coerce", dayfirst=True)
    if pd.isna(tanggal_lahir):
        return None

    return tanggal_lahir.to_pydatetime() if hasattr(tanggal_lahir, "to_pydatetime") else tanggal_lahir


def _build_alamat_detail(row: pd.Series) -> str:
    alamat = "" if is_empty(_get(row, COLUMN_MAP["alamat"])) else str(_get(row, COLUMN_MAP["alamat"])).strip()
    rt = normalize_digits(_get(row, COLUMN_MAP["rt"]))
    rw = normalize_digits(_get(row, COLUMN_MAP["rw"]))
    kelurahan = _normalize_kelurahan(_get(row, COLUMN_MAP["kelurahan"]))

    parts: list[str] = []
    if alamat:
        parts.append(alamat)

    rt_rw = ""
    if rt and rw:
        rt_rw = f"RT {rt}/RW {rw}"
    elif rt:
        rt_rw = f"RT {rt}"
    elif rw:
        rt_rw = f"RW {rw}"

    if rt_rw:
        parts.append(rt_rw)

    if kelurahan:
        parts.append(kelurahan)

    return ", ".join(parts)


def map_row_to_patient(row: pd.Series) -> Patient:
    return Patient(
        nik=_normalize_nik(_get(row, COLUMN_MAP["nik"])),
        nama=_normalize_name(_get(row, COLUMN_MAP["nama"])),
        tanggal_lahir=_normalize_birth_date(_get(row, COLUMN_MAP["tanggal_lahir"])),
        jenis_kelamin=_normalize_gender(_get(row, COLUMN_MAP["jenis_kelamin"])),
        no_wa=normalize_phone(_get(row, COLUMN_MAP["no_telp"])),
        kelurahan=_normalize_kelurahan(_get(row, COLUMN_MAP["kelurahan"])),
        alamat_detail=_build_alamat_detail(row),
    )
