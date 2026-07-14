from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any

from app.business.customer.mapper.customer_mapper import CustomerMapper
from app.business.goal.mapper.goal_mapper import GoalMapper
from app.business.portfolio.mapper.portfolio_mapper import PortfolioMapper
from app.dtos.request_context import RequestContext
from app.mapper.llm_response_mapper import LLMResponseMapper
from app.mapper.workflow_execution_mapper import WorkflowExecutionMapper
from app.workflows.advisor.advisor_state import AdvisorState


class AdvisorStateMapper:

    @classmethod
    def from_dict(
        cls,
        state: AdvisorState | dict,
    ) -> AdvisorState:

        if isinstance(state, AdvisorState):
            return state

        state = dict(state)

        if state.get("request") is not None:
            state["request"] = cls._request(
                state["request"],
            )


        if state.get("goal_analysis") is not None:
            state["goal_analysis"] = GoalMapper.from_dict(
                state["goal_analysis"],
            )

        if state.get("workflow_execution") is not None:
            state["workflow_execution"] = (
                WorkflowExecutionMapper.from_dict(
                    state["workflow_execution"],
                )
            )

        if state.get("llm_response") is not None:
            state["llm_response"] = LLMResponseMapper.from_dict(state["llm_response"])

        return AdvisorState(**state)

    @staticmethod
    def _request(
        request: RequestContext | dict,
    ) -> RequestContext:

        if isinstance(request, RequestContext):
            return request

        return RequestContext(**request)