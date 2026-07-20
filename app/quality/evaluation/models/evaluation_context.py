from dataclasses import dataclass

from app.models.conversation import Conversation
from app.models.feedback import Feedback
from app.models.message import Message


@dataclass(slots=True, kw_only=True)
class EvaluationContext:
    conversation: Conversation

    user_message: Message

    assistant_message: Message

    feedback: Feedback | None

    trace: Trace