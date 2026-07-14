from pydantic import BaseModel

class SourceResponse(BaseModel):
    source_id: int
    scheme_name: str
    document_type: str
    section_name: str | None
    page_no: int | None