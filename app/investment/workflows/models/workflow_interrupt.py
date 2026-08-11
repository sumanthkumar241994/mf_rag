from typing import Any, Generic, TypeVar

from pydantic import Field

from app.investment.base.models import InvestmentBaseModel
from app.investment.common.enums.interrupt_type import (
    InterruptType,
)

T = TypeVar("T")


class WorkflowInterrupt(InvestmentBaseModel):
    type: InterruptType
    title: str
    message: str
    data: Any | None = Field(default=None)

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")
    
    def to_message(self) -> str:

        return (
            f"{self.title}\n\n"
            f"{self.message}"
        )