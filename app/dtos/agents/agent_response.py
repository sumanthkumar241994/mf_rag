from typing import Any
from dataclasses import dataclass, field
from uuid import UUID
from app.business.document.models.retrieval_response import SourceResponse
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt

@dataclass(slots=True)
class AgentResponse:
    conversation_id: UUID
    answer: str | None = None
    
    workflow_interrupt: WorkflowInterrupt | None = None
    chunk_count: int | None = None
    response_time_ms: int | None = None
    sources: list[SourceResponse] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
   

    @property
    def interrupted(self) -> bool:
        return self.workflow_interrupt is not None