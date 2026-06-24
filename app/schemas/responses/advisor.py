from pydantic import BaseModel

class SourceResponse(BaseModel):
    source_id: int
    scheme_name: str
    document_type: str
    section_name: str | None
    page_no: int | None

class AdvisorResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]

    chunk_count: int | None = None
    response_time_ms: int | None = None