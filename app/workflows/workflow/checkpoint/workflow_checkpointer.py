from __future__ import annotations

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from app.core.config import settings

serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        (
            "app.business.portfolio.models.goal_portfolio_snapshot",
            "GoalPortfolioSnapshot",
        ),
        (
            "app.workflows.workflow.models.goal_workflow_payload",
            "GoalWorkflowPayload",
        ),
        (
            "app.workflows.workflow.models.workflow_interrupt",
            "WorkflowInterrupt",
        ),
        (
            "app.workflows.workflow.models.workflow_execution",
            "WorkflowExecution",
        ),
        "app.business.goal.models",
        "app.business.portfolio.models",
        "app.business.advisor.models",
        "app.workflows.workflow.models",
        "app.business.advisor.enums",
        "app.business.portfolio.analysis.models"
    ]
)


class WorkflowCheckpointer:

    def __init__(self):
        self._checkpointer: AsyncPostgresSaver | None = None

    async def initialize(self) -> None:

        if self._checkpointer is not None:
            return

        self._context = AsyncPostgresSaver.from_conn_string(
            settings.POSTGRES_CHECKPOINT_URL,
            serde=serde
        )

        self._checkpointer = await self._context.__aenter__()

        await self._checkpointer.setup()

    @property
    def checkpointer(
        self,
    ) -> AsyncPostgresSaver:

        if self._checkpointer is None:
            raise RuntimeError(
                "Workflow checkpointer is not initialized."
            )

        return self._checkpointer

    async def shutdown(self) -> None:

        if self._context is not None:
            await self._context.__aexit__(
                None,
                None,
                None,
            )

        self._context = None
        self._checkpointer = None