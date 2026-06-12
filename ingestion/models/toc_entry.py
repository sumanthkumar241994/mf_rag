from dataclasses import dataclass

@dataclass(slots=True)
class TOCEntry:
    title: str
    start_page: int