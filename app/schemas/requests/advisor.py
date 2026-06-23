from pydantic import BaseModel

class AdvisorRequest(BaseModel):
    query: str
    top_k: int = 5
    scheme_name: str | None = None
    document_type: str | None = None
