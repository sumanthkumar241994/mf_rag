from dataclasses import dataclass


@dataclass(slots=True)
class DocumentSection:
    title: str
    content: str
    page_number: int
    