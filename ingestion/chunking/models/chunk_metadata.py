from dataclasses import dataclass

@dataclass(slots=True)
class ChunkMetadata:
    section_title: str
    section_category: str
    page_number: int
    chunk_order: int
    