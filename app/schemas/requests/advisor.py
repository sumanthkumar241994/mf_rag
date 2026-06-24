from pydantic import BaseModel

class AdvisorRequest(BaseModel):
    query: str
