from deepeval.metrics import AnswerRelevancyMetric, BiasMetric, ContextualPrecisionMetric, FaithfulnessMetric, HallucinationMetric, ToxicityMetric
from deepeval.metrics.contextual_relevancy.contextual_relevancy import ContextualRelevancyMetric
from app.api.dependencies.llm import get_llm_gateway
from app.prompts.evaluator.builder.planner_judge_prompt_builder import PlannerJudgePromptBuilder
from app.prompts.registry import PromptRegistry
from app.quality.evaluation.deepeval.adapter import DeepEvalAdapter
from app.quality.evaluation.deepeval.llm import AdvisorJudgeLLM
from app.quality.evaluation.enums import MetricType
from app.quality.evaluation.evaluation_service import EvaluationService
from app.quality.evaluation.evaluator.cost_evaluator import CostEvaluator
from app.quality.evaluation.evaluator.deepeval_evaluator import DeepEvalEvaluator
from app.quality.evaluation.evaluator.latency_evaluator import LatencyEvaluator
from app.quality.evaluation.evaluator.planner_evaluator import PlannerEvaluator
from app.quality.evaluation.evaluator_registry import EvaluatorRegistry
from app.quality.evaluation.judges.planner_judge import PlannerJudge


def get_evaluation_service() -> EvaluationService:
    registry = EvaluatorRegistry()
    llm_gateway=get_llm_gateway()

    prompt_registry=PromptRegistry()

    planner_judge = PlannerJudge(
        llm_gateway=llm_gateway,
        prompt_registry=prompt_registry
        
    )

    judge_llm = AdvisorJudgeLLM(
        gateway = llm_gateway
    )

    adapter = DeepEvalAdapter(
    metrics={
        MetricType.ANSWER_RELEVANCY: AnswerRelevancyMetric(
            model=judge_llm,
            threshold=0.7,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
        MetricType.FAITHFULNESS: FaithfulnessMetric(
            model=judge_llm,
            threshold=0.7,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
        MetricType.CONTEXTUAL_RELEVANCY: ContextualRelevancyMetric(
            model=judge_llm,
            threshold=0.7,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
        MetricType.CONTEXTUAL_PRECISION: ContextualPrecisionMetric(
            model=judge_llm,
            threshold=0.7,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
        MetricType.HALLUCINATION: HallucinationMetric(
            model=judge_llm,
            threshold=0.2,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
        MetricType.BIAS: BiasMetric(
            model=judge_llm,
            threshold=0.2,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
        MetricType.TOXICITY: ToxicityMetric(
            model=judge_llm,
            threshold=0.2,
            include_reason=True,
            async_mode=True,
            strict_mode=False,
            verbose_mode=False,
        ),
    }
)

    prompt_registry.register(PlannerJudgePromptBuilder())

    # registry.register(
    #     LatencyEvaluator(),
    # )

    # registry.register(
    #     CostEvaluator(),
    # )

    # registry.register(
    #     PlannerEvaluator(planner_judge),
    # )
    
    registry.register(
        DeepEvalEvaluator(adapter=adapter)
    )
    

    # registry.register(
    #     PromptEvaluator(),
    # )

    # registry.register(
    #     ResponseEvaluator(),
    # )

    evaluation_service = EvaluationService(
        registry,
    )

    return evaluation_service