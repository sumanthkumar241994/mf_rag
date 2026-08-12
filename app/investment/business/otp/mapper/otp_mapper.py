

from app.investment.business.otp.models.verification_result import SendOTPResult, VerifyOTPResult


class VerificationMapper:

    def send_otp_result_mapper(
        self,
        data: dict,
    ) -> SendOTPResult:

        return SendOTPResult(
            success=data.get("status") == 1,
            message=data.get("message"),
        )
    
    def verify_otp_result_mapper(
        self,
        data: dict,
    ) -> VerifyOTPResult:

        return VerifyOTPResult(
            success=data.get("status") == 1,
            message=data.get("message"),
            verification_id=data.get("customer_action_uid")
        )