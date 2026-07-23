import time

from app.models.evaluation import EvaluationModel
from app.models.evaluation_metric import EvaluationMetricModel
from app.notifications.notification_service import NotificationService
from app.quality.evaluation import issue_analyzer
from app.quality.evaluation.enums import EvaluationStatus, MetricStatus
from app.quality.evaluation.evaluator_registry import EvaluatorRegistry
from app.quality.evaluation.issue_analyzer import IssueAnalyzer
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric
from app.quality.evaluation.models.evaluation_result import EvaluationResult
from app.unit_of_work.evaluation_uow import EvaluationUnitOfWork
from app.unit_of_work.evaluation_uow_factory import EvaluationUnitOfWorkFactory


class EvaluationService:

    EVALUATOR_VERSION = "1.0.0"

    def __init__(
        self,
        registry: EvaluatorRegistry,
        issue_analyzer: IssueAnalyzer,
        notification_service: NotificationService,
        uow_factory: EvaluationUnitOfWorkFactory,
    ):
        self._registry = registry
        self._issue_analyzer = issue_analyzer
        self._uow_factory = uow_factory
        self._notification_service = notification_service

    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:
        self.uow = await self._uow_factory.create()

        start = time.perf_counter()

        metrics: list[EvaluationMetric] = []

        for evaluator in self._registry.evaluators:
            result = await evaluator.evaluate(context)
            metrics.extend(result.metrics)

        duration = int((time.perf_counter() - start) * 1000)

        scores = [
            metric.score
            for metric in metrics
            if metric.score is not None
        ]

        overall_score = (
            sum(scores) / len(scores)
            if scores
            else None
        )

        status = (
            EvaluationStatus.FAILED
            if any(metric.status == MetricStatus.FAILED for metric in metrics)
            else EvaluationStatus.COMPLETED
        )

        evaluation_result = EvaluationResult(
            metrics=metrics,
            overall_score=overall_score,
            status=status,
            duration_ms=duration,
        )
        async with self.uow:
            await self._create_evaluation(
                context=context,
                result=evaluation_result,
            )

        event = await self._issue_analyzer.analyze(
            context=context,
            result=evaluation_result,
        )

        if event:
            await self._notification_service.publish(event)

        return evaluation_result


    async def _create_evaluation(
        self,
        context: EvaluationContext,
        result: EvaluationResult,
    ) -> None:

        evaluation = EvaluationModel(
            conversation_id=context.conversation.id,
            message_id=context.assistant_message.id,
            trace_id=context.trace.trace_id,
            status=result.status,
            overall_score=result.overall_score,
            trigger_type=context.trigger_type,
            evaluator_version=self.EVALUATOR_VERSION,
        )

        evaluation.metrics = [
            EvaluationMetricModel(
                metric=metric.type,
                source=metric.source,
                status=metric.status,
                score=metric.score,
                reason=metric.explanation,
                _metadata=metric.metadata,
            )
            for metric in result.metrics
        ]

        await self.uow.evaluations.create(evaluation)