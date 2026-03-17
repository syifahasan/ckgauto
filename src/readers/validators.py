import math
from typing import Any


def is_empty(value: Any) -> bool:
    return value is None or str(value).strip() == "" or (isinstance(value, float) and math.isnan(value))


def require_value(value: Any, field_name: str) -> Any:
    if is_empty(value):
        raise ValueError(f"Field wajib kosong: {field_name}")
    return value


def normalize_digits(value: Any) -> str:
    """
    Pertahankan hanya digit. Aman untuk NIK, RT/RW, no RM numerik, dll.
    """
    if is_empty(value):
        return ""

    text = str(value).strip()

    # kasus angka dari excel menjadi float, mis. 3212114401600005.0
    if isinstance(value, float):
        text = str(int(value))

    return "".join(ch for ch in text if ch.isdigit())


def normalize_phone(value: Any) -> str:
    """
    Bersihkan nomor telepon/WA.
    Nilai seperti 0, 00, 0000 dianggap kosong.
    """
    digits = normalize_digits(value)

    # jika kosong atau terlalu pendek
    if digits == "" or len(digits) < 9:
        return ""

    return digits
