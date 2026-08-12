from pydantic import BaseModel


class VerifyOTPResult(BaseModel):
    success: bool
    message: str | None = None
    verification_id: str | None = None

class SendOTPResult(BaseModel):
    success: bool
    message: str | None = None