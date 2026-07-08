from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Token:
    text: str
    position: str
    normalized: str