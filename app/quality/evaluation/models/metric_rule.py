from dataclasses import dataclass

from app.notifications.models import NotificationSeverity


@dataclass(slots=True)
class MetricRule:
    threshold: float
    severity: NotificationSeverity