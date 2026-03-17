from config.constants import DEFAULT_PHONE


def normalize_phone_number(nomor: str) -> str:
    nomor = str(nomor).strip()
    if not nomor:
        return DEFAULT_PHONE
    if nomor.startswith("0"):
        return nomor[1:]
    if nomor.startswith("+62"):
        return nomor[3:]
    if nomor.startswith("62"):
        return nomor[2:]
    
    if len(nomor) < 9:
        return DEFAULT_PHONE
    return nomor
