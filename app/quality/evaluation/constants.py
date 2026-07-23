from app.notifications.models import NotificationSeverity
from app.quality.evaluation.enums import MetricType
from app.quality.evaluation.models.metric_rule import MetricRule


RULES = {
    MetricType.PLANNER_ACCURACY: MetricRule(
        threshold=0.5,
        severity=NotificationSeverity.MEDIUM,
    ),
    MetricType.ANSWER_RELEVANCY: MetricRule(
        threshold=0.6,
        severity=NotificationSeverity.MEDIUM,
    ),
    MetricType.FAITHFULNESS: MetricRule(
        threshold=0.6,
        severity=NotificationSeverity.HIGH,
    ),
    MetricType.CONTEXTUAL_RELEVANCY: MetricRule(
        threshold=0.6,
        severity=NotificationSeverity.MEDIUM,
    ),
    MetricType.CONTEXTUAL_PRECISION: MetricRule(
        threshold=0.6,
        severity=NotificationSeverity.MEDIUM,
    ),
    MetricType.HALLUCINATION: MetricRule(
        threshold=0.3,
        severity=NotificationSeverity.CRITICAL,
    ),
    MetricType.BIAS: MetricRule(
        threshold=0.3,
        severity=NotificationSeverity.HIGH,
    ),
    MetricType.TOXICITY: MetricRule(
        threshold=0.3,
        severity=NotificationSeverity.CRITICAL,
    ),
}