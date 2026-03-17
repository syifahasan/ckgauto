from dataclasses import dataclass


@dataclass
class ConfirmationResult:
    total_pages: int = 0
    total_confirmed: int = 0
    total_skipped: int = 0
