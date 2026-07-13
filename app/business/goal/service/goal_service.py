from __future__ import annotations

from app.business.advisor.enums import tool_type
from app.business.advisor.enums.capabilities import Capability
from app.business.goal.analyzer.goal_analyzer import GoalAnalyzer
from app.business.goal.calculator.goal_calculator import GoalCalculator
from app.business.goal.context.goal_context_provider import GoalContextProvider
from app.business.goal.enums.goal_type import GoalType
from app.business.goal.mapper.goal_mapper import GoalMapper
from app.business.goal.models.goal import Goal
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.parser.goal_parser import GoalParser
from app.business.goal.parser.goal_resume_parser import GoalResumeParser
from app.business.goal.resolver.parameter_resolver import ParameterResolver
from app.business.common.services.base_workflow_service import (
    BaseWorkflowService,
)
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.goal_workflow_payload import (
    GoalWorkflowPayload,
)
from app.workflows.workflow.models.workflow_execution import (
    WorkflowExecution,
)
from app.workflows.workflow.models.workflow_resume import WorkflowResume
from app.workflows.workflow.service.workflow_service import WorkflowService


class GoalService(BaseWorkflowService[GoalAnalysis]):

    def __init__(
        self,
        parser: GoalParser,
        resume_parser: GoalResumeParser,
        resolver: ParameterResolver,
        calculator: GoalCalculator,
        analyzer: GoalAnalyzer,
        workflow_service: WorkflowService,
        context_provider: GoalContextProvider
    ):
        super().__init__(workflow_service)

        self._parser = parser
        self._resume_parser = resume_parser
        self._resolver = resolver
        self._calculator = calculator
        self._analyzer = analyzer
        self._context_provider = context_provider

    async def analyze(
        self,
        state: AdvisorState,
    ) -> WorkflowExecution[GoalAnalysis]:

        await self._context_provider.enrich(state)

        goal, parameters = self._parser.parse(
            query=state.request.query,
            goal_type=self._goal_capability(state)
        )

        return self._process(
            state=state,
            goal=goal,
            parameters=parameters,
        )

    async def resume(
        self,
        state: AdvisorState,
        payload: GoalWorkflowPayload,
        resume: WorkflowResume,
    ) -> WorkflowExecution[GoalAnalysis]:

        await self._context_provider.enrich(state)
        analysis = GoalMapper.from_dict(payload.analysis)
        parameters = self._resume_parser.update(
            parameters=analysis.parameters,
            missing_parameters=analysis.parameter_resolution.missing_parameters,
            answer=resume.answer
        )

        return self._process(
            state=state,
            goal=analysis.goal,
            parameters=parameters,
        )

    def _process(
        self,
        state: AdvisorState,
        goal: Goal,
        parameters: GoalParameters,
    ) -> WorkflowExecution[GoalAnalysis]:

        parameters, resolution = self._resolver.resolve(
            parameters=parameters,
            customer=state.customer,
            portfolio_analysis=state.portfolio_analysis,
        )

        projection = None

        if resolution.complete:
            projection = self._calculator.calculate(
                parameters,
            )

        analysis = self._analyzer.analyze(
            goal=goal,
            parameters=parameters,
            resolution=resolution,
            projection=projection,
        )

        execution = self._create_workflow_execution(
            state=state,
            capability=Capability.GOAL,
            result=analysis,
            complete=resolution.complete,
        )

        state.goal_analysis = analysis
        state.workflow_execution = execution

        return execution

    def _goal_capability(
        self,
        state: AdvisorState,
    ) -> GoalType:
        _CAPABILITY_TO_GOAL = {
                Capability.RETIREMENT.value: GoalType.RETIREMENT,
                Capability.CHILD_EDUCATION.value: GoalType.EDUCATION
            }
        for capability in state.planner_result.capabilities:
            if capability.capability in (
                Capability.RETIREMENT,
                Capability.CHILD_EDUCATION,
                Capability.WEALTH_CREATION,
                Capability.EMERGENCY_FUND,
            ):
            
                return _CAPABILITY_TO_GOAL[capability.capability]

        raise ValueError("Goal capability not found.")