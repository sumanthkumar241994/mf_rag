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
        (
            "app.business.portfolio.analysis.models.portfolio_analysis",
            "PortfolioAnalysis",
        ),
        ('app.investment.business.customer.models.customer', 'Customer'),
        ('app.business.customer.enums.kyc_status', 'KYCStatus'),
        ('app.investment.business.customer.enums.onboarding_status', 'OnboardingStatus'),
        ('app.investment.business.customer.enums.signature_status', 'SignatureStatus'),
        ('app.investment.business.customer.enums.address_type', 'AddressType'),
        ('app.investment.business.customer.enums.source_of_wealth_code', 'SourceOfWealthCode'),
        ('app.investment.business.customer.enums.annual_income_code', 'AnnualIncomeCode'),
        ('app.investment.business.customer.enums.nominee_identity_type', 'NomineeIdentityType'),
        ('app.investment.business.customer.enums.marital_status', 'MaritalStatus'),
        ('app.investment.business.customer.enums.kyc_status', 'KYCStatus'),
        ('app.investment.business.customer.enums.gender', 'Gender'),
        ('app.investment.workflows.models.workflow_execution', 'WorkflowExecution'),
        ('app.investment.common.enums.interrupt_type', 'InterruptType'),
        ('app.investment.models.action_type', 'NextAction'),
        ('app.investment.common.enums.action_type', 'ActionType'),
        ('app.dtos.request_context', 'RequestContext'),
        ('app.investment.models.eligibility', 'Eligibility'),
        ('app.investment.common.enums.requirement_status', 'RequirementStatus'),
        ('app.investment.common.enums.eligibility_requirement_type', 'EligibilityRequirementType'),
        ('app.investment.workflows.models.workflow_execution', 'WorkflowExecution[Customer]'),
        ('app.investment.common.enums.operation_type', 'OperationType'),
        ('app.investment.business.execution.goal.update_nominee_execution_goal', 'UpdateNomineeExecutionGoal'),
        ('app.investment.business.customer.enums.occupation_code', 'OccupationCode'),
        ('app.investment.business.execution.goal.update_fatca_execution_goal', 'UpdateFatcaExecutionGoal'),
        ('app.investment.business.otp.enums.verification_purpose', 'VerificationPurpose'),
        ('app.investment.business.otp.models.verification_state', 'VerificationState'),
        ('asyncpg.pgproto.pgproto', 'UUID'),
        "app.business.goal.models",
        "app.business.portfolio.models",
        "app.business.advisor.models",
        "app.workflows.workflow.models",
        "app.business.advisor.enums",
        # Investment
        "app.investment.models",
        "app.investment.workflows.models",
        "app.investment.business.customer.models",
        "app.investment.business.customer.enums",
        "app.investment.business.execution.goal",
        "app.investment.common.enums",
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