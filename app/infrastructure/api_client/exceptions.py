
from app.common.exceptions.infrastructure_exception import InfrastructureException


class HttpClientError(InfrastructureException):
    """Base exception for all API client errors."""

    def __init__(
        self,
        message: str,
        *,
        code: str = 'http_client_error',
        status_code: int | None = None,
        retryable: bool = False
    ) -> None:
        super().__init__(message, code)
        self.retryable = retryable
        self.status_code = status_code

    def __str__(self) -> str:
        parts = []
        if self.code:
            parts.append(self.code)
        if self.status_code is not None:
            parts.append(str(self.status_code))
        
        prefix=''
        if parts:
            prefix = f"[{'/'.join(parts)}]"

        return f"{prefix}{self.message}"


class AuthenticationError(HttpClientError):
    """Authentication with external service failed."""

    def __init__(
        self,
        message: str = "Authentication failed.",
    ) -> None:
        super().__init__(
            message, 
            status_code=401,
            code='authentication_failed',
        )


class AuthorizationError(HttpClientError):
    """Authorization with external service failed."""

    def __init__(
        self,
        message: str = "Authorization failed.",
    ) -> None:
        super().__init__(
            message, 
            status_code=403,
            code='authroization_failed',
        )


class ResourceNotFoundError(HttpClientError):
    """Requested resource was not found."""

    def __init__(
        self,
        message: str = "Requested resource was not found.",
    ) -> None:
        super().__init__(
            message, 
            status_code=404,
            code='resource_not_found'
        )


class ValidationError(HttpClientError):
    """Request validation failed."""

    def __init__(
        self,
        message: str = "Validation failed.",
    ) -> None:
        super().__init__(
            message, 
            status_code=422,
            code='validation_failed'
        )


class RequestTimeoutError(HttpClientError):
    """Request to external service timed out."""

    def __init__(
        self,
        message: str = "Request timed out.",
    ) -> None:
        super().__init__(
            message, 
            status_code=408,
            code='request_timeout',
            retryable=True
        )


class ServiceUnavailableError(HttpClientError):
    """External service is unavailable."""

    def __init__(
        self,
        message: str = "External service is unavailable.",
    ) -> None:
        super().__init__(
            message, 
            status_code=503,
            code='service_unavailable',
            retryable=True
        )


class ApiClientError(HttpClientError):
    """Unexpected API client error."""

    def __init__(
        self,
        message: str = "Unexpected API client error.",
    ) -> None:
        super().__init__(
            message,
            code='api_client_error'
        )