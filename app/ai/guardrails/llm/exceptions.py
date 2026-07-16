from app.common.exceptions.business_exception import BusinessException


class LLMGuardParserError(BusinessException):
    """Raised when the LLM Guard response cannot be parsed."""
    def __init__(self, message: str, code: str | None = None):
         super().__init__(
            message=message,
            code=code,
        )