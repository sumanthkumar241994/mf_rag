from app.quality.evaluation.evaluator.base_evalutor import BaseEvaluator


class EvaluatorRegistry:

    def __init__(self):
        self._evaluators: list[BaseEvaluator] = []

    def register(
        self,
        evaluator: BaseEvaluator,
    ) -> None:
        self._evaluators.append(evaluator)

    @property
    def evaluators(
        self,
    ) -> list[BaseEvaluator]:
        return self._evaluators