from dataclasses import dataclass

@dataclass(slots=True)
class SemanticSegment:
    title: str
    content: str
    page_number: int