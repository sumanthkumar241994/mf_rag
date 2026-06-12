from dataclasses import dataclass
from .page import Page


@dataclass(slots=True)
class ParsedDocument:
    file_name: str
    source_path: str
    page_count: int
    pages: list[Page]
    full_text: str
    metadata: dict
