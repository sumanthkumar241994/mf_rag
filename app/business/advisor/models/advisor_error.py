from dataclasses import dataclass

from app.business.common.models.gateway_result import GatewayError


@dataclass(slots=True)
class AdvisorError:
    code: str
    message: str
    retryable: bool = False
    source: str | None = None
    fatal: bool = False
    retry_count: int = 0

    # from_gateway() → expected runtime/business failures.
    @classmethod
    def from_gateway(cls, error: GatewayError, *, source: str, fatal: bool=False) -> "AdvisorError":
        return cls(
            code=error.code,
            message=error.message,
            retryable=error.retryable,
            source=source,
            fatal=fatal
        )
        
    # from_exception() → unexpected programming/runtime failures.
    @classmethod
    def from_exception(cls, exception: Exception, *, source: str, fatal: bool=False) -> "AdvisorError":
        return cls(
            code=getattr(exception, "code", exception.__class__.__name__),
            message=str(exception),
            retryable=getattr(exception, 'retryable', False),
            source=source,
            fatal=fatal
        )