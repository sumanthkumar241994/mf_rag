from dataclasses import dataclass

@dataclass
class SemanticSegment:
    title: str
    content: str
    page_number: int