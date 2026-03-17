from dataclasses import dataclass


@dataclass
class RegistrationResult:
    total_rows: int = 0
    registered: int = 0
    skipped: int = 0
    failed: int = 0
