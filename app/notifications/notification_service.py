from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID
from app.notifications.base import BaseNotificationClient
from app.notifications.enums import NotificationType
from app.notifications.models import NotificationEvent
from app.quality.feedback.enums.insight import FeedbackIssueAction
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.feedback_insight import FeedbackInsight
from app.quality.feedback.models.feedback_issue import FeedbackIssue
from app.quality.feedback.models.feedback_occurence import FeedbackOccurrence


class NotificationService:

    def __init__(
        self,
        client: BaseNotificationClient,
    ):
        self._client = client

    async def publish(
        self,
        event: NotificationEvent,
    ) -> None:

        await self._client.notify(event)

    from app.notifications.base import BaseNotificationClient
from app.notifications.models import NotificationEvent
from app.quality.feedback.enums.insight import FeedbackIssueAction
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.feedback_insight import FeedbackInsight
from app.quality.feedback.models.feedback_issue import FeedbackIssue
from app.quality.feedback.models.feedback_occurence import FeedbackOccurrence


class NotificationService:

    def __init__(
        self,
        client: BaseNotificationClient,
    ):
        self._client = client

    async def publish(
        self,
        event: NotificationEvent,
    ) -> None:

        await self._client.notify(event)

    async def publish_feedback_issue(
        self,
        issue: FeedbackIssue,
        occurrence: FeedbackOccurrence,
        insight: FeedbackInsight,
        feedback: Feedback,
        action: FeedbackIssueAction,
    ) -> None:

        event = NotificationEvent(
            event=(
                "feedback.issue.created"
                if action == FeedbackIssueAction.CREATED
                else "feedback.issue.updated"
            ),
            severity=issue.severity,
            title=f"Feedback Issue - {insight.category}",
            description=insight.summary,
            notification_type=(
                NotificationType.FEEDBACK_ISSUE_CREATED
                if action == FeedbackIssueAction.CREATED
                else NotificationType.FEEDBACK_ISSUE_UPDATED
            ),


            metadata={
                "issue": self.to_dict(issue),
                "occurrence": occurrence.model_dump(mode="json"),
                "feedback": feedback.model_dump(mode="json"),
                "insight": self.to_dict(insight),
            },
        )

        await self.publish(event)

    @classmethod
    def to_dict(cls, obj: Any) -> dict[str, Any]:
        if not is_dataclass(obj):
            raise TypeError(f"{type(obj).__name__} is not a dataclass")

        return cls._serialize(asdict(obj))

    @classmethod
    def _serialize(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: cls._serialize(val)
                for key, val in value.items()
            }

        if isinstance(value, list):
            return [cls._serialize(item) for item in value]

        if isinstance(value, tuple):
            return tuple(cls._serialize(item) for item in value)

        if isinstance(value, UUID):
            return str(value)

        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, Enum):
            return value.value

        return value