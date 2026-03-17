from dataclasses import dataclass


@dataclass
class ServiceResult:
    total_pages: int = 0
    total_started: int = 0
    total_completed: int = 0
    total_failed: int = 0
