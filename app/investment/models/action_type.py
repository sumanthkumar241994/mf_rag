from typing import Any
from pydantic import BaseModel, Field

from app.investment.common.enums.action_type import ActionType


class NextAction(BaseModel):
    action: ActionType
    payload: Any | None = None
    interrupt: bool = False