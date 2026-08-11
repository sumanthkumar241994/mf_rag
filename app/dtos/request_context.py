from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

@dataclass(slots=True)
class RequestContext:
    query: str | None = None
    customer_id: str | None = None
    conversation_id: UUID | None = None
    workflow_resume: Any | None = None