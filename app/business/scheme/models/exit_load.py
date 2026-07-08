from dataclasses import dataclass


@dataclass(slots=True)
class ExitLoad:
    percentage: float