
from dataclasses import dataclass, field
from typing import Any

from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.advisor.models.planner_result import PlannerResult
from app.business.advisor.models.prompt import Prompt
from app.business.customer.models.customer import Customer
from app.business.document.models.llm_context import LLMContext
from app.business.document.models.retrieval_response import SourceResponse
from app.business.goal.mapper.goal_mapper import GoalMapper
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis
from app.business.scheme.models.scheme_details import SchemeDetails
from app.business.scheme.models.scheme_query import SchemeQuery
from app.compliance.prompt.models.prompt_compliance_result import PromptComplianceResult
from app.compliance.response.streaming.stream_state import StreamState
from app.dtos.llm.llm_response import LLMResponse
from app.dtos.request_context import RequestContext
from app.dtos.workflow.tool_execution_result import ToolExecutionResult
from app.investment.workflows.models.delegation import Delegation
from app.mapper.planner_result_mapper import PlannerResultMapper
from app.mapper.workflow_execution_mapper import WorkflowExecutionMapper
from app.schemas.conversation.cache_message import CacheMessage
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt


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

    delegation: Delegation | None = None

    guardrail_result: GuardRailResult | None = None
    
    prompt_compliance_result: PromptComplianceResult | None = None

    #planner
    planner_result : PlannerResult | None = None

    # Customer
    customer: Customer | None = None
    # Domain results
    portfolio_analysis: PortfolioAnalysis | None = None

    goal_analysis: GoalAnalysis | None = None
    
    scheme_query: SchemeQuery | None = None
    schemes: list[SchemeDetails] | None = None

    # workflow
    workflow_execution : WorkflowExecution | None = None

    workflow_interrupt: WorkflowInterrupt | None = None

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


    def restore(self) -> None:
        
        if isinstance(self.request, dict):
            self.request = RequestContext(**self.request)

        if self.errors:
            self.errors = [
                error
                if isinstance(error, AdvisorError)
                else AdvisorError(**error)
                for error in self.errors
        ]

        if isinstance(self.planner_result, dict):
            self.planner_result = PlannerResultMapper.from_dict(
                self.planner_result
            )

        if isinstance(self.workflow_execution, dict):
            self.workflow_execution = WorkflowExecutionMapper.from_dict(
                self.workflow_execution
            )

        if isinstance(self.goal_analysis, dict):
            self.goal_analysis = GoalMapper.from_dict(
                self.goal_analysis
            )



