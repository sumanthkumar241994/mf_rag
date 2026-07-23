from dataclasses import dataclass
from datetime import datetime

from app.langfuse.models.trace_context import TraceContext
from app.models.conversation import Conversation
from app.models.feedback import Feedback
from app.models.message import Message
from app.quality.evaluation.enums import EvaluationTriggerType


@dataclass(slots=True, kw_only=True)
class EvaluationContext:
    evaluation_id: str | None = None
    trigger_type: EvaluationTriggerType = EvaluationTriggerType.FEEDBACK
    conversation: Conversation
    user_message: Message
    assistant_message: Message
    feedback: Feedback | None = None
    trace: TraceContext
    created_at: datetime | None = None