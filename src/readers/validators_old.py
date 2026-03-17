import math
from typing import Any


def is_empty(value: Any) -> bool:
    return value is None or str(value).strip() == "" or (isinstance(value, float) and math.isnan(value))


def require_value(value: Any, field_name: str) -> Any:
    if is_empty(value):
        raise ValueError(f"Field wajib kosong: {field_name}")
    return value
