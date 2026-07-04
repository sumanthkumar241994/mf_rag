from app.common.exceptions.advisor_exception import AdvisorException


class BusinessException(AdvisorException):
    """
    Base exception for business/domain failures.
    """
    def __init__(
        self,
        message: str,
        code: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
        )