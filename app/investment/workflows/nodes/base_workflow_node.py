from __future__ import annotations

from typing import Generic, TypeVar

from app.investment.base.models import GatewayResult, WorkflowError
from app.investment.workflows.investment_state import InvestmentState

T = TypeVar("T")


class BaseWorkflowNode(Generic[T]):
    """
    Base class for Investment workflow nodes.

    Provides common functionality for:
    - Handling gateway failures
    - Storing workflow execution
    - Determining whether a workflow should continue
    """

    @staticmethod
    def handle_gateway_result(
        *,
        state: InvestmentState,
        result: GatewayResult[T],
        source: str,
    ) -> T | None:
        """
        Processes a GatewayResult.

        On failure:
            - clears the current workflow execution
            - records a WorkflowError
            - returns None

        On success:
            - returns the underlying data
        """

        if result.success:
            return result.data

        state.workflow_execution = None

        state.add_error(
            WorkflowError.from_gateway(
                error=result.error,
                source=source,
            )
        )

        return None