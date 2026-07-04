# app/common/exceptions/base.py

class AdvisorException(Exception):
    """
    Base exception for the Advisor Platform.
    """

    def __init__(self, message: str, code: str  | None = None):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message