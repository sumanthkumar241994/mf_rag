from dataclasses import dataclass


@dataclass(slots=True)
class Usage:
    input: int
    output: int
    total: int