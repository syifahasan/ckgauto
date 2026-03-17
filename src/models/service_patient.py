from dataclasses import dataclass
from typing import Optional


@dataclass
class ServicePatient:
    nik: str
    nama: str = ""
    bb: Optional[float] = None
    tb: Optional[float] = None
    sistol: Optional[int] = None
    diastol: Optional[int] = None
    gds: Optional[int] = None