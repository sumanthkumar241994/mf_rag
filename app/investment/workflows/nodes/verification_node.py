from typing import Any

from langgraph.types import interrupt

from app.investment.business.execution.customer.planners.customer_update_stage import OperationActionMapper
from app.investment.business.otp.models.verification_result import VerifyOTPResult
from app.investment.common.enums.action_type import ActionType
from app.investment.business.otp.models.verification_request import (
    VerificationRequest,
)
from app.investment.business.otp.models.verification_state import (
    VerificationState,
)
from app.investment.workflows.investment_state import InvestmentState
from app.mcp.client.otp_client import OTPClient


class VerificationNode:

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

        # No OTP required for this execution goal.
        if not goal.requires_verification:
            return state

        action = OperationActionMapper.map(goal.operation)

        # ---------------------------------------------------------
        # If there is a pending customer action, make sure the
        # verification is associated with that action.
        #
        # Example:
        #
        # pending_action = NOMINEE
        # execution_goal = UPDATE_NOMINEE
        # verification.action = UPDATE_NOMINEE
        # ---------------------------------------------------------
        self._validate_pending_action(
            state=state,
            action=action,
        )

        # ---------------------------------------------------------
        # Already verified for this action.
        # ---------------------------------------------------------
        if self._is_already_verified(
            state=state,
            action=action,
        ):
            return state

        # ---------------------------------------------------------
        # Send OTP only once.
        #
        # otp_sent is persisted in the checkpoint.
        # ---------------------------------------------------------
        if self._requires_otp_send(
            state=state,
            action=action,
        ):
            verification = await self._send_otp(
                state=state,
                action=action,
            )
            state.verification = verification

        # ---------------------------------------------------------
        # Wait for OTP.
        #
        # First execution:
        #     interrupt() pauses the graph.
        #
        # Resume:
        #     interrupt() returns the resume payload.
        # ---------------------------------------------------------
        resume_data = interrupt(
            self._build_interrupt(
                state=state,
                action=action,
            )
        )

        otp = self._extract_otp(
            resume_data,
        )

        # ---------------------------------------------------------
        # Verify OTP.
        # ---------------------------------------------------------
        result = await self._verify_otp(
            state=state,
            action=action,
            otp=otp,
        )

        # ---------------------------------------------------------
        # OTP failed.
        # ---------------------------------------------------------
        if not result.success:

            # Don't reset otp_sent here.
            #
            # The same verification session can be used
            # for another OTP attempt.
            #
            # If the OTP service tells us that the session
            # has expired/exhausted attempts, reset it.
            if self._should_reset_verification(result):
                self._reset_verification(state)

            interrupt(
                {
                    "type": "otp_verification",
                    "action": action.value,
                    "title": "OTP Verification",
                    "message": (
                        result.data
                        or "Invalid OTP. Please try again."
                    ),
                }
            )

            return state

        # ---------------------------------------------------------
        # OTP successfully verified.
        # ---------------------------------------------------------
        verification = state.verification

        if verification is None:
            raise ValueError(
                "Verification state is missing."
            )

        verification_id = result.data.verification_id

        if not verification_id:
            raise ValueError(
                "Customer action ID was not returned "
                "after OTP verification."
            )

        verification.verified = True
        verification.verification_id = verification_id

        return state

    # =============================================================
    # OTP
    # =============================================================

    async def _send_otp(
        self,
        state: InvestmentState,
        action: ActionType,
    ) -> None:

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
            conversation_id=str(state.request.conversation_id),
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
        # IMPORTANT:
        #
        # customer_action_id is NOT available after send OTP.
        #
        # It is returned only after OTP verification.
        # ---------------------------------------------------------
        verification = VerificationState(
            required=True,
            otp_sent=True,
            verified=False,
            verification_id=None,
            action=action,
            purpose=goal.verification_purpose,
            payload=payload,
        )

        return verification

    async def _verify_otp(
        self,
        state: InvestmentState,
        action: ActionType,
        otp: str,
    ):

        verification = state.verification

        if verification is None:
            raise ValueError(
                "Verification state is missing."
            )

        payload = {
            **verification.payload,
            "otp": otp,
        }

        request = VerificationRequest(
            trace_id=state.trace_id,
            conversation_id=str(state.request.conversation_id),
            customer_id=state.request.customer_id,
            action=action,
            purpose=(
                verification.purpose
                or state.execution_goal.verification_purpose
            ),
            payload=payload,
        )

        return await self._otp_client.verify_otp(
            request=request,
        )

    # =============================================================
    # Pending action
    # =============================================================

    @staticmethod
    def _validate_pending_action(
        state: InvestmentState,
        action: ActionType,
    ) -> None:
        """
        Ensures that the execution being verified corresponds
        to the currently selected pending action.

        pending_actions:
            All outstanding requirements.

        pending_action:
            Requirement currently being processed.
        """

        pending_action = state.pending_action

        if pending_action is None:
            return

        # If NextAction contains the ActionType directly.
        if (
            pending_action.action is not None
            and pending_action.action != action
        ):
            raise ValueError(
                "Verification action does not match "
                "the selected pending action."
            )

    # Verification state
    @staticmethod
    def _is_already_verified(
        state: InvestmentState,
        action: ActionType,
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
        action: ActionType,
    ) -> bool:

        verification = state.verification

        if verification is None:
            return True

        # Different action → new verification session.
        if verification.action != action:
            return True

        # Already sent → don't send again.
        if verification.otp_sent:
            return False

        return True

    @staticmethod
    def _reset_verification(
        state: InvestmentState,
    ) -> None:

        if state.verification is None:
            return

        state.verification.otp_sent = False
        state.verification.verified = False
        state.verification.verification_id = None

    # =============================================================
    # Helpers
    # =============================================================

    @staticmethod
    def _extract_otp(
        resume_data: Any,
    ) -> str:

        if isinstance(resume_data, str):
            otp = resume_data.strip()

        elif isinstance(resume_data, dict):
            otp = str(
                resume_data.get("otp", "")
            ).strip()

        else:
            otp = ""

        if not otp:
            raise ValueError(
                "OTP is required."
            )

        return otp

    @staticmethod
    def _build_interrupt(
        state: InvestmentState,
        action: ActionType,
    ) -> dict:

        pending_action = state.pending_action

        return {
            "type": "otp_verification",
            "action": action.value,
            "pending_action": (
                pending_action.action
                if pending_action
                else None
            ),
            "title": "OTP Verification",
            "message": (
                "Please enter the OTP sent to "
                "your registered mobile number."
            ),
        }

    @staticmethod
    def _build_verification_payload(
        state: InvestmentState,
        action: ActionType,
    ) -> dict[str, Any]:

        # The execution goal should provide the provider-specific
        # payload.
        goal = state.execution_goal

        if goal is None:
            raise ValueError(
                "Execution goal is required."
            )

        return goal.verification_payload(
            customer=state.customer,
        )

    @staticmethod
    def _should_reset_verification(
        result,
    ) -> bool:

        # Adapt this to the status returned by your OTP service.
        return getattr(
            result,
            "status",
            None,
        ) in {
            "expired",
            "max_attempts",
        }