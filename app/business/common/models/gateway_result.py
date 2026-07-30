from dataclasses import dataclass
from typing import Generic, TypeVar

T =TypeVar("T")

@dataclass(slots=True, frozen=True)
class GatewayError:
    code: str
    message: str
    retryable: bool = False


@dataclass(slots=True, frozen=True)
class GatewayResult(Generic[T]):
    success: bool
    data: T | None = None
    error: GatewayError | None = None

    @classmethod
    def ok(cls, data: T) -> "GatewayResult[T]":
        return cls(success=True, data=data)
    
    @classmethod
    def failure(cls, code: str, message: str, retryable: bool = False) -> "GatewayResult[T]":
        return cls(
            success=False,
            error=GatewayError(
                code=code,
                message=message,
                retryable=retryable
            )
        )
    
    @classmethod
    def from_error(cls, error: GatewayError) -> "GatewayResult[T]":
        return cls(success=False, error=error)