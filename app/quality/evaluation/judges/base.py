from abc import ABC, abstractmethod

from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.judge_models import JudgeResult



class BaseJudge(ABC):

    @abstractmethod
    async def judge(
        self,
        context: EvaluationContext,
    ) -> JudgeResult:
        pass