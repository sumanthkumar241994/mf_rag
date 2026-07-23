from dataclasses import dataclass


@dataclass(slots=True)
class Cost:
    total: float