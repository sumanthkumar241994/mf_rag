from uuid import UUID
from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    chunk_id: UUID
    content: str
    scheme_name: str
    amc_name: str
    document_type: str
    section_name: str | None = None
    page_no: int | None = None
    score: float | None = None


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 10
    scheme_name: str | None = None
    document_type: str | None = None