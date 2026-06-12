from dataclasses import dataclass


@dataclass(slots=True)
class Chunk:
    content: str
    section_name: str
    page_number: int
    token_count: int
    chunk_hash: str
    