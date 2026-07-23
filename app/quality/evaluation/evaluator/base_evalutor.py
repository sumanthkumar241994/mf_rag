from abc import ABC, abstractmethod

from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_result import EvaluationResult



class BaseEvaluator(ABC):
    @abstractmethod
    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:
        pass