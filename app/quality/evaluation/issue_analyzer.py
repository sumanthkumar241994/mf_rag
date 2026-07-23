from collections import defaultdict

from app.notifications.models import (
    NotificationEvent,
    NotificationSeverity,
)
from app.quality.evaluation.constants import RULES
from app.quality.evaluation.enums import MetricType
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_result import EvaluationResult
from app.quality.evaluation.models.metric_rule import MetricRule


class IssueAnalyzer:

    CRITICAL_METRICS = {
        MetricType.HALLUCINATION,
        MetricType.TOXICITY,
    }

    MIN_NON_CRITICAL_FAILURES = 2

    def __init__(
        self,
        rules: dict[MetricType, MetricRule] = RULES,
    ) -> None:
        self._rules = rules

    async def analyze(
        self,
        context: EvaluationContext,
        result: EvaluationResult,
    ) -> NotificationEvent | None:

        critical_failures = []
        non_critical_failures = []

        highest_severity = NotificationSeverity.LOW

        for metric in result.metrics:

            if metric.score is None:
                continue

            rule = self._rules.get(metric.type)

            if rule is None:
                continue

            if metric.type in (
                MetricType.HALLUCINATION,
                MetricType.TOXICITY,
            ):
                failed = metric.score >= rule.threshold
            else:
                failed = metric.score < rule.threshold

            if not failed:
                continue

            if rule.severity == NotificationSeverity.CRITICAL:
                highest_severity = NotificationSeverity.CRITICAL
            elif (
                highest_severity != NotificationSeverity.CRITICAL
                and rule.severity == NotificationSeverity.HIGH
            ):
                highest_severity = NotificationSeverity.HIGH
            elif (
                highest_severity
                not in (
                    NotificationSeverity.CRITICAL,
                    NotificationSeverity.HIGH,
                )
                and rule.severity == NotificationSeverity.MEDIUM
            ):
                highest_severity = NotificationSeverity.MEDIUM

            if metric.type in self.CRITICAL_METRICS:
                critical_failures.append(metric)
            else:
                non_critical_failures.append(metric)

        should_create = (
            len(critical_failures) > 0
            or len(non_critical_failures) >= self.MIN_NON_CRITICAL_FAILURES
        )

        if not should_create:
            return None

        failures = critical_failures + non_critical_failures

        description = "\n".join(
            f"- {metric.type.value}: {metric.score:.2f}"
            + (
                f" ({metric.explanation})"
                if metric.explanation
                else ""
            )
            for metric in failures
        )

        return NotificationEvent(
            event="evaluation_failed",
            severity=highest_severity,
            title=f"[{highest_severity.value.upper()}] AI Evaluation Failed",
            description=description,
            metadata={
                "evaluation_id": context.evaluation_id,
                "trace_id": str(context.trace.trace_id),
                "conversation_id": str(context.conversation.id),
                "customer_id": context.conversation.customer_id,
                "query": context.user_message.content,
                "assistant_response": context.assistant_message.content,
                "failed_metrics": [
                    {
                        "type": metric.type.value,
                        "score": metric.score,
                        "status": metric.status.value,
                        "explanation": metric.explanation,
                    }
                    for metric in failures
                ],
            },
        )