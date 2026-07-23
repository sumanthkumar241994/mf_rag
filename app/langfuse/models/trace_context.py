from dataclasses import dataclass

from .generation_context import GenerationContext
from .planner_context import PlannerContext
from .prompt_context import PromptContext
from .retrieval_context import RetrievalContext


@dataclass(slots=True)
class TraceContext:
    trace_id: str
    planner: PlannerContext | None = None
    retrieval: RetrievalContext | None = None
    prompt: PromptContext | None = None
    planner_generation: GenerationContext | None = None
    advisor_generation: GenerationContext | None = None