from dataclasses import dataclass
from datetime import datetime

@dataclass
class Patient:
    nik: str
    nama: str
    tanggal_lahir: datetime
    jenis_kelamin: str
    no_wa: str
    kelurahan: str
    alamat_detail: str