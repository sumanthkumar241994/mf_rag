from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.notifications.enums import NotificationType


class NotificationSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class NotificationEvent:
    event: str
    severity: NotificationSeverity

    title: str
    description: str
    notification_type: NotificationType | None = None
    metadata: dict[str, Any] = field(default_factory=dict)