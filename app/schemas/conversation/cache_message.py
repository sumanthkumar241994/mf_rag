from pydantic import BaseModel, Field

class CacheMessage(BaseModel):
    role: str
    content: str
    metadata: dict = Field(default_factory=dict)