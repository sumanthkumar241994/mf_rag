from app.investment.business.execution.customer.planners.customer_update_stage import (
    OperationActionMapper,
)
from app.investment.business.otp.models.verification_request import (
    VerificationRequest,
)
from app.investment.business.otp.models.verification_state import (
    VerificationState,
)
from app.investment.workflows.investment_state import InvestmentState
from app.mcp.client.otp_client import OTPClient


class VerificationPrepareNode:
    """
    Prepares an OTP verification session for the current
    execution goal.

    Responsibilities:
    - Validate execution goal.
    - Validate pending action.
    - Reuse an existing OTP session when possible.
    - Send OTP when required.
    - Populate state.verification.

    IMPORTANT:
    This node does NOT call interrupt().

    It must return normally after state.verification is populated
    so LangGraph can checkpoint the verification state before
    VerificationWaitNode interrupts.
    """

    def __init__(
        self,
        otp_client: OTPClient,
    ) -> None:
        self._otp_client = otp_client

    async def __call__(
        self,
        state: InvestmentState,
    ) -> InvestmentState:

        goal = state.execution_goal

        if goal is None:
            raise ValueError(
                "Execution goal is required for verification."
            )

        # ---------------------------------------------------------
        # No OTP required for this execution goal.
        # ---------------------------------------------------------

        if not goal.requires_verification:
            return state

        action = OperationActionMapper.map(
            goal.operation,
        )

        # ---------------------------------------------------------
        # Make sure the verification action matches the currently
        # selected pending action.
        # ---------------------------------------------------------

        self._validate_pending_action(
            state=state,
            action=action,
        )

        # ---------------------------------------------------------
        # Already verified for this action.
        #
        # This can happen if the workflow reaches this node again
        # after verification has already completed.
        # ---------------------------------------------------------

        if self._is_already_verified(
            state=state,
            action=action,
        ):
            return state

        # ---------------------------------------------------------
        # Existing OTP session.
        #
        # If OTP was already sent and the customer has not verified
        # it yet, don't send another OTP.
        # ---------------------------------------------------------

        if not self._requires_otp_send(
            state=state,
            action=action,
        ):
            return state

        # ---------------------------------------------------------
        # Send OTP.
        # ---------------------------------------------------------

        verification = await self._send_otp(
            state=state,
            action=action,
        )

        # ---------------------------------------------------------
        # IMPORTANT:
        #
        # This mutation happens BEFORE the node returns.
        #
        # LangGraph can now checkpoint:
        #
        # state.verification.verification_id
        # state.verification.otp_sent
        # state.verification.action
        # state.verification.purpose
        # state.verification.payload
        #
        # before VerificationWaitNode calls interrupt().
        # ---------------------------------------------------------

        state.verification = verification

        return state

    # =============================================================
    # OTP
    # =============================================================

    async def _send_otp(
        self,
        state: InvestmentState,
        action,
    ) -> VerificationState:

        goal = state.execution_goal

        if goal is None:
            raise ValueError(
                "Execution goal is required."
            )

        payload = self._build_verification_payload(
            state=state,
            action=action,
        )

        request = VerificationRequest(
            trace_id=state.trace_id,
            conversation_id=str(
                state.request.conversation_id,
            ),
            customer_id=state.request.customer_id,
            action=action,
            purpose=goal.verification_purpose,
            payload=payload,
        )

        result = await self._otp_client.send_otp(
            request=request,
        )

        if not result.success:
            raise ValueError(
                result.error.message
                if result.error
                else "Unable to send OTP."
            )

        # ---------------------------------------------------------
        # customer_action_id / verification_id is NOT expected
        # from send OTP according to your current API contract.
        #
        # It is populated after OTP verification.
        # ---------------------------------------------------------

        return VerificationState(
            required=True,
            otp_sent=True,
            verified=False,
            verification_id=None,
            action=action,
            purpose=goal.verification_purpose,
            payload=payload,
        )

    # =============================================================
    # Pending action
    # =============================================================

    @staticmethod
    def _validate_pending_action(
        state: InvestmentState,
        action,
    ) -> None:

        pending_action = state.pending_action

        if pending_action is None:
            return

        if (
            pending_action.action is not None
            and pending_action.action != action
        ):
            raise ValueError(
                "Verification action does not match "
                "the selected pending action."
            )

    # =============================================================
    # Verification state
    # =============================================================

    @staticmethod
    def _is_already_verified(
        state: InvestmentState,
        action,
    ) -> bool:

        verification = state.verification

        if verification is None:
            return False

        return (
            verification.required
            and verification.verified
            and verification.action == action
            and verification.verification_id is not None
        )

    @staticmethod
    def _requires_otp_send(
        state: InvestmentState,
        action,
    ) -> bool:

        verification = state.verification

        if verification is None:
            return True

        # Different action means a new verification session.
        if verification.action != action:
            return True

        # OTP already sent for this action.
        if verification.otp_sent:
            return False

        return True

    # =============================================================
    # Helpers
    # =============================================================

    @staticmethod
    def _build_verification_payload(
        state: InvestmentState,
        action,
    ) -> dict:

        goal = state.execution_goal

        if goal is None:
            raise ValueError(
                "Execution goal is required."
            )

        return goal.verification_payload(
            customer=state.customer,
        )