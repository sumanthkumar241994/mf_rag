from typing import Any
from app.investment.business.customer.models.fatca import Fatca
from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.customer.customer_data_collection_registry import CustomerDataCollectionBuilderRegistry
from app.investment.business.execution.goal.update_fatca_execution_goal import UpdateFatcaExecutionGoal
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal
from app.investment.common.enums.eligibility_requirement_type import EligibilityRequirementType
from app.investment.common.enums.interrupt_type import InterruptType
from app.investment.models.action_type import NextAction
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

        if not state.pending_actions:
            return state

        # =========================================================
        # If no action has been selected yet, ask the customer
        # which pending requirement they want to complete.
        #
        # Example:
        #
        # pending_actions:
        #   NOMINEE
        #   FATCA
        #
        # interrupt:
        #   "Please complete the following steps..."
        # =========================================================

        if state.pending_action is None:

            resume_data = interrupt(
                self._build_pending_actions_interrupt(
                    state,
                )
            )

            state.workflow_resume = resume_data

            state.pending_action = (
                self._resolve_pending_action(
                    state=state,
                    resume_data=resume_data,
                )
            )
        # =========================================================
        # A pending action is selected.
        #
        # Build the actual missing-data response.
        #
        # Example:
        #
        # Customer selected NOMINEE
        #
        # response:
        #   existing_data
        #   missing_fields
        # =========================================================

        requirement = self._requirement_for_action(
            state.pending_action,
        )

        builder = self._registry.get(
            requirement,
        )

        data = builder.build(state)

        workflow_interrupt = WorkflowInterrupt(
            type=InterruptType.COLLECT_DATA,
            title=data.title,
            message=data.message,
            data=data,
        )

        # ---------------------------------------------------------
        # Interrupt and wait for the actual customer data.
        # ---------------------------------------------------------

        resume_data = interrupt(
            workflow_interrupt.model_dump(
                mode="json",
            )
        )

        # ---------------------------------------------------------
        # Customer submitted the requested data.
        # ---------------------------------------------------------

        self._apply_resume_data(
            state=state,
            requirement=requirement,
            resume_data=resume_data,
        )

        # The data collection interaction is complete.
        state.workflow_resume = None

        return state

    # =============================================================
    # Pending actions summary
    # =============================================================

    @staticmethod
    def _build_pending_actions_interrupt(
        state: InvestmentState,
    ) -> dict[str, Any]:

        return {
            "type": InterruptType.COLLECT_DATA.value,
            "title": "Additional information required",
            "message": (
                "Please complete the following steps "
                "before continuing."
            ),
            "data": [
                DataCollectionNode._pending_action_to_dict(
                    action,
                )
                for action in state.pending_actions
            ],
        }

    @staticmethod
    def _pending_action_to_dict(
        action: NextAction,
    ) -> dict[str, Any]:

        requirement = action.payload

        if hasattr(
            requirement,
            "model_dump",
        ):
            requirement = requirement.model_dump(
                mode="json",
            )

        return {
            "action": action.action.value,
            "data": requirement,
        }

    @staticmethod
    def _resolve_pending_action(
        state: InvestmentState,
        resume_data: Any,
    ) -> NextAction:

        if not isinstance(
            resume_data,
            dict,
        ):
            raise ValueError(
                "Invalid workflow resume payload."
            )

        action_value = resume_data.get(
            "action",
        )

        if not action_value:
            raise ValueError(
                "Action is required."
            )

        # ---------------------------------------------------------
        # "continue" means take the first pending action.
        # ---------------------------------------------------------

        if action_value == "continue":

            return state.pending_actions[0]

        # ---------------------------------------------------------
        # Customer explicitly selected an action.
        # ---------------------------------------------------------

        for action in state.pending_actions:

            if action.action.value == action_value:
                return action

        raise ValueError(
            f"Unsupported pending action: {action_value}"
        )
    
    @staticmethod
    def _requirement_for_action(
        action: NextAction,
    ) -> EligibilityRequirementType:

        requirement = action.payload

        if isinstance(
            requirement,
            dict,
        ):
            code = requirement.get(
                "code",
            )
        else:
            code = getattr(
                requirement,
                "code",
                None,
            )

        if code is None:
            raise ValueError(
                "Eligibility requirement code is missing."
            )

        if isinstance(
            code,
            EligibilityRequirementType,
        ):
            return code

        try:
            return EligibilityRequirementType(
                code,
            )
        except ValueError as exc:
            raise ValueError(
                f"Unsupported eligibility requirement: {code}"
            ) from exc


    def _apply_resume_data(
    self,
    state: InvestmentState,
    requirement: EligibilityRequirementType,
    resume_data: dict,
    ) -> None:

        if not isinstance(resume_data,dict) :
            raise ValueError(
                "Invalid data collection payload."
            )

        data = resume_data.get("data")
        if data is None:
            raise ValueError("Collected data is missing.")

        if requirement == EligibilityRequirementType.NOMINEE:

            nominee = Nominee.model_validate(
                resume_data["data"]
            )

            state.execution_goal = UpdateNomineeExecutionGoal(
                customer_id=state.request.customer_id,
                nominee=nominee,
            )

            return

        if requirement == EligibilityRequirementType.FATCA:

            fatca = Fatca.model_validate(
                resume_data["data"]
            )

            state.execution_goal = UpdateFatcaExecutionGoal(
                customer_id=state.request.customer_id,
                fatca=fatca,
            )

            return

        raise ValueError(
            f"Unsupported requirement: {requirement}"
        )