from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PIIFinding:
    type: str
    value: str
    replacement: str