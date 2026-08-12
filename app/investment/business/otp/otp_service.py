
from app.infrastructure.api_client.models import GateWayRequestContext
from app.investment.base.models import GatewayResult
from app.investment.business.otp.gateway.otp_gateway import VerificationGateway
from app.investment.business.otp.mapper.otp_mapper import VerificationMapper
from app.investment.business.otp.models.verification_request import VerificationRequest
from app.investment.business.otp.models.verification_result import SendOTPResult, VerifyOTPResult
from app.observability.tracing import trace_step


class OTPVerificationService:

    def __init__(
        self,
        verification_gateway: VerificationGateway,
        verification_mapper: VerificationMapper,
    ):
        self._verification_gateway = verification_gateway
        self._verification_mapper = verification_mapper

    @trace_step(
        "verification_service",
        output_mapper=lambda result: {
            "success": result.success,
        },
        metadata_mapper=lambda _: {
            "service": "verification",
        },
    )
    async def send_otp(
        self,
        request: VerificationRequest,
    ) -> GatewayResult[SendOTPResult]:

        gateway_context = GateWayRequestContext(
            trace_id=request.trace_id,
            conversation_id=request.conversation_id,
            customer_id=request.customer_id,
        )

        result = await self._verification_gateway.send_otp(
            context=gateway_context,
            payload=request.payload,
        )

        if not result.success:
            return GatewayResult.failure(
                code=result.error.code,
                message=result.error.message,
            )

        verification = self._verification_mapper.send_otp_result_mapper(
            result.data,
        )

        return GatewayResult.ok(
            verification,
        )

    @trace_step(
        "verification_service",
        output_mapper=lambda result: {
            "success": result.success,
            "verification_id": (
                result.data.verification_id
                if result.success and result.data
                else None
            ),
        },
        metadata_mapper=lambda _: {
            "service": "verification",
        },
    )
    async def verify_otp(
        self,
        request: VerificationRequest,
    ) -> GatewayResult[VerifyOTPResult]:

        gateway_context = GateWayRequestContext(
            trace_id=request.trace_id,
            conversation_id=request.conversation_id,
            customer_id=request.customer_id,
        )

        result = await self._verification_gateway.verify_otp(
            context=gateway_context,
            payload=request.payload
        )

        if not result.success:
            return GatewayResult.failure(
                code=result.error.code,
                message=result.error.message,
            )

        verification = self._verification_mapper.verify_otp_result_mapper(
            result.data,
        )
        print(verification)

        return GatewayResult.ok(
            verification
        )