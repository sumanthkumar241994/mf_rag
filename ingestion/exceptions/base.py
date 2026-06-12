
class IngestionException(Exception):
    """
    Base exception for all ingestion-related errors
    """

    def __init__(self, message: str, error_code: str | None = None) -> None:
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        
        return self.message
