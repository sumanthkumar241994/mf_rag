from dataclasses import dataclass

@dataclass(slots=True)
class SectionBoundary:
    title: str
    start_page: int
    start_line: int
    end_page: int
    end_line: int