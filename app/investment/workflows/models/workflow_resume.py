from typing import Any
from pydantic import BaseModel, Field


class WorkflowResume(BaseModel):
    action: str
    data: dict[str, Any] = Field(
        default_factory=dict,
    )