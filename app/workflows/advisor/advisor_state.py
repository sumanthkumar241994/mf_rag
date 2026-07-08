
from dataclasses import dataclass, field
from typing import Any

from app.business.advisor.enums.agent_type import AgentType
from app.business.advisor.enums.intent import Intent
from app.business.advisor.enums.tool_type import ToolType
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.advisor.models.planner_result import PlannerResult
from app.business.advisor.models.prompt import Prompt
from app.business.approval.models.approval_context import ApprovalContext
from app.business.portfolio.analysis.models import insight
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis
from app.business.scheme.models.scheme_details import SchemeDetails
from app.business.scheme.models.scheme_query import SchemeQuery
from app.dtos.llm.llm_response import LLMResponse
from app.dtos.request_context import RequestContext
from app.dtos.retrieval.llm_context import LLMContext
from app.dtos.workflow.tool_execution_result import ToolExecutionResult
from app.schemas.conversation.cache_message import CacheMessage
from app.schemas.responses.advisor import SourceResponse


@dataclass(slots=True)
class AdvisorState:
    """
    Shared state that flows through the advisor workflow.
    Every analyzer, planner, tool and agent enriches this object.
    """

    # Request
    request: RequestContext

    history: list[CacheMessage] = field(default_factory=list)

    trace_id: str | None = None

    #planner
    planner_result : PlannerResult | None = None

    # Domain results
    portfolio_analysis: PortfolioAnalysis | None = None
    
    scheme_query: SchemeQuery | None = None
    schemes: list[SchemeDetails] | None = None

    # memory
    #memory: MemoryContext | None = None 

    # Human in loop
    #approval: ApprovalContext | None = None

    # Retrieval
    llm_context: LLMContext | None = None

    sources: list[SourceResponse] = field(default_factory=list)

    chunk_count: int = 0

    # Generation
    prompt: Prompt | None = None
    llm_response: LLMResponse | None = None

    # Evaluation
    #evaluation: EvaluationResult | None = None

    tool_results: list[ToolExecutionResult] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)
    # retrieval

    errors: list[AdvisorError] = field(default_factory=list)

    def add_error(self, error: AdvisorError):
        for index, existing in enumerate(self.errors):
            if existing.source == error.source:
                self.errors[index] = error
                return
        self.errors.append(error)

    
    def get_latest_error(self, source: str) -> AdvisorError | None:
        for error in reversed(self.errors):
            if error.source == source:
                return error
            
        return None
    
    def clear_error(self, source: str):
        self.errors = [error for error in self.errors if error.source != source]



