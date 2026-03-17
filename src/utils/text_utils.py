def normalize_gender(value: str) -> str:
    value = (value or "").strip().lower()
    if value in {"l", "laki-laki", "laki laki"}:
        return "Laki-Laki"
    if value in {"p", "perempuan"}:
        return "Perempuan"
    return value.title()
