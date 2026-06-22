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
    distance: float | None = None