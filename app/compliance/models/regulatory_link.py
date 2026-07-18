from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegulatoryLink:
    title: str
    url: str