from app.common.exceptions.business_exception import BusinessException


class PlannerParserError(BusinessException):

    def __init__(self, message: str, code: str | None = None):
         super().__init__(
            message=message,
            code=code,
        )