from dataclasses import dataclass

from app.models.conversation import Conversation
from app.models.message import Message
from app.quality.feedback.models.feedback import Feedback


@dataclass(slots=True, kw_only=True)
class FeedbackInsightContext:
    feedback: Feedback
    conversation: Conversation
    user_message: Message
    assistant_message: Message
    planner_result: dict | None = None