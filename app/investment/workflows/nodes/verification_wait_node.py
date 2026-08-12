from typing import Any

from langgraph.types import interrupt

from app.investment.business.execution.customer.planners.customer_update_stage import (
    OperationActionMapper,
)
from app.investment.business.otp.models.verification_request import (
    VerificationRequest,
)
from app.investment.workflows.investment_state import InvestmentState
from app.mcp.client.otp_client import OTPClient


class VerificationWaitNode:
    """
    Waits for the customer to provide the OTP and verifies it.

    Responsibilities:
    - Validate persisted verification state.
    - Interrupt and wait for OTP.
    - Extract OTP from workflow resume payload.
    - Verify OTP.
    - Update verification state.

    This node assumes VerificationPrepareNode has already
    created and checkpointed state.verification.
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

        if not goal.requires_verification:
            return state

        verification = state.verification

        if verification is None:
            raise ValueError(
                "Verification state is missing."
            )

        action = OperationActionMapper.map(
            goal.operation,
        )

        self._validate_pending_action(
            state=state,
            action=action,
        )

        # ---------------------------------------------------------
        # Already verified.
        # ---------------------------------------------------------

        if self._is_already_verified(
            state=state,
            action=action,
        ):
            return state

        # ---------------------------------------------------------
        # Verification session must have OTP sent.
        # ---------------------------------------------------------

        if not verification.otp_sent:
            raise ValueError(
                "OTP has not been sent for the current "
                "verification session."
            )

        # ---------------------------------------------------------
        # Wait for OTP.
        #
        # First execution:
        #     interrupt() pauses the graph.
        #
        # Resume:
        #     interrupt() returns workflow_resume.
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

            # -----------------------------------------------------
            # If the OTP session has expired or attempts are
            # exhausted, reset the verification session.
            #
            # Otherwise preserve the same session so the customer
            # can retry.
            # -----------------------------------------------------

            if self._should_reset_verification(
                result,
            ):
                self._reset_verification(
                    state,
                )

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

        state.verification.verified = True

        # customer_action_uid from the provider is mapped to
        # verification_id by VerificationResultMapper.
        state.verification.verification_id = verification_id

        return state

    # =============================================================
    # OTP verification
    # =============================================================

    async def _verify_otp(
        self,
        state: InvestmentState,
        action,
        otp: str,
    ):

        verification = state.verification

        if verification is None:
            raise ValueError(
                "Verification state is missing."
            )

        goal = state.execution_goal

        if goal is None:
            raise ValueError(
                "Execution goal is required."
            )

        payload = {
            **verification.payload,
            "otp": otp,
        }

        request = VerificationRequest(
            trace_id=state.trace_id,
            conversation_id=str(
                state.request.conversation_id,
            ),
            customer_id=state.request.customer_id,
            action=action,
            purpose=(
                verification.purpose
                or goal.verification_purpose
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
    def _reset_verification(
        state: InvestmentState,
    ) -> None:

        verification = state.verification

        if verification is None:
            return

        verification.otp_sent = False
        verification.verified = False
        verification.verification_id = None

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
        action,
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
    def _should_reset_verification(
        result,
    ) -> bool:

        return getattr(
            result,
            "status",
            None,
        ) in {
            "expired",
            "max_attempts",
        }