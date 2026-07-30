from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")
E = TypeVar("E", bound=BaseModel)

class InvestmentBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        use_enum_values=False,
    )


class RequestContext(BaseModel):
    query: str 
    customer_id: str 
    conversation_id: UUID 
    workflow_resume: str | None  = None

class GatewayError(InvestmentBaseModel):
    code: str
    message: str
    retryable: bool = False


class GatewayResult(GenericModel, Generic[T]):
    success: bool
    data: T | None = None
    error: GatewayError | None = None

    @classmethod
    def ok(cls, data: T) -> "GatewayResult[T]":
        return cls(
            success=True,
            data=data,
        )

    @classmethod
    def failure(
        cls,
        code: str,
        message: str,
        retryable: bool = False,
    ) -> "GatewayResult[T]":
        return cls(
            success=False,
            error=GatewayError(
                code=code,
                message=message,
                retryable=retryable,
            ),
        )

    @classmethod
    def from_error(
        cls,
        error: GatewayError,
    ) -> "GatewayResult[T]":
        return cls(
            success=False,
            error=error,
        )


class WorkflowError(InvestmentBaseModel):
    code: str
    message: str
    retryable: bool = False
    source: str | None = None
    fatal: bool = False
    retry_count: int = Field(default=0, ge=0)

    @classmethod
    def from_gateway(
        cls,
        error: GatewayError,
        *,
        source: str,
        fatal: bool = False,
    ) -> "WorkflowError":
        return cls(
            code=error.code,
            message=error.message,
            retryable=error.retryable,
            source=source,
            fatal=fatal,
        )

    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        *,
        source: str,
        fatal: bool = False,
    ) -> "WorkflowError":
        return cls(
            code=getattr(exception, "code", exception.__class__.__name__),
            message=str(exception),
            retryable=getattr(exception, "retryable", False),
            source=source,
            fatal=fatal,
        )