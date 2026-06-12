from dataclasses import dataclass

@dataclass(slots=True)
class SectionMarker:
    title: str
    page_number: int
    line_number: int
    