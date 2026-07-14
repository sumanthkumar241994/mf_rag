from dataclasses import asdict, dataclass, field
from typing import Any

from app.business.advisor.enums.tool_type import ToolType
from app.dtos.llm.llm_stream_response import LLMStreamResponse
from app.enums.stream_event_type import StreamEventType
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt
from fastapi.encoders import jsonable_encoder

@dataclass(slots=True)
class AgentStreamEvent:
    type: StreamEventType
    token: str | None = None
    tool: ToolType | None = None
    success: bool | None = None
    message: str | None = None
    response: LLMStreamResponse | None = None
    workflow_interrupt: WorkflowInterrupt | None = None
    metadata: dict[str, Any] | None = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "type": self.type,
        }

        if self.token is not None:
            payload["token"] = self.token

        if self.tool is not None:
            payload["tool"] = str(
                self.tool.value if hasattr(self.tool, "value") else self.tool
            )

        if self.success is not None:
            payload["success"] = self.success

        if self.message is not None:
            payload["message"] = self.message

        if self.response is not None:
            payload["response"] = self.response.to_dict()

        if self.metadata:
            payload["metadata"] = self.metadata

        if self.workflow_interrupt is not None:
            payload["workflow_interrupt"] = {
                "capability": self.workflow_interrupt.capability.value,
                "questions": self.workflow_interrupt.questions
            }
    

        return payload