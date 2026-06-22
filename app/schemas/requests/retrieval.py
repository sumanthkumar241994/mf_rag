from pydantic import BaseModel


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 10
    scheme_name: str | None = None
    document_type: str | None = None