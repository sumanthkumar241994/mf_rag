from abc import ABC, abstractmethod

from app.quality.feedback.models.feedback_insight_context import FeedbackInsightContext
from app.quality.feedback.models.feedback_insight_result import FeedbackInsightResult


class FeedbackInsightEvaluator(ABC):

    @abstractmethod
    async def evaluate(
        self,
        context: FeedbackInsightContext,
    ) -> FeedbackInsightResult:
        raise NotImplementedError