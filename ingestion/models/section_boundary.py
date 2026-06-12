from dataclasses import dataclass

@dataclass(slots=True)
class SectionBoundary:
    title: str
    normalized_title: str
    start_page: int
    end_page: int