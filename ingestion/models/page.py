from dataclasses import dataclass

@dataclass(slots=True)
class Page:
    page_number: int
    content: str
    char_count: int