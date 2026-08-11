from app.investment.business.customer.models.fatca import Fatca
from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.customer.customer_data_collection_registry import CustomerDataCollectionBuilderRegistry
from app.investment.business.execution.goal.update_fatca_execution_goal import UpdateFatcaExecutionGoal
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal
from app.investment.common.enums.eligibility_requirement_type import EligibilityRequirementType
from app.investment.common.enums.interrupt_type import InterruptType
from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt
from langgraph.types import interrupt


class DataCollectionNode:

    def __init__(
        self,
        registry: CustomerDataCollectionBuilderRegistry,
    ):
        self._registry = registry

    async def __call__(
        self,
        state: InvestmentState,
    ) -> InvestmentState:

        eligibility = state.eligibility

        if eligibility is None:
            raise ValueError(
                "Eligibility is not available."
            )

        requirement = eligibility.required[0]

        builder = self._registry.get(
            requirement.code,
        )

        data = builder.build(state)

        workflow_interrupt = WorkflowInterrupt(
            type=InterruptType.COLLECT_DATA,
            title=data.title,
            message=data.message,
            data=data,
        )

        state.workflow_execution = WorkflowExecution(
            result=eligibility,
            interrupt=workflow_interrupt,
        )

        resume_data = interrupt(
            workflow_interrupt.model_dump(mode="json")
        )

        state.workflow_execution = None

        self._apply_resume_data(
            state=state,
            requirement=requirement.code,
            resume_data=resume_data,
        )

        return state

    def _apply_resume_data(
    self,
    state: InvestmentState,
    requirement: EligibilityRequirementType,
    resume_data: dict,
    ) -> None:

        if requirement == EligibilityRequirementType.NOMINEE:

            nominee = Nominee.model_validate(
                resume_data["data"]
            )

            state.execution_goal = UpdateNomineeExecutionGoal(
                customer_id=state.customer.id,
                nominee=nominee,
            )

            return

        if requirement == EligibilityRequirementType.FATCA:

            fatca = Fatca.model_validate(
                resume_data["data"]
            )

            state.execution_goal = UpdateFatcaExecutionGoal(
                customer_id=state.customer.id,
                fatca=fatca,
            )

            return

        raise ValueError(
            f"Unsupported requirement: {requirement}"
        )