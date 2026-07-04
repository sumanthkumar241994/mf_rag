from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class GateWayRequestContext:
    trace_id: str | None = None
    conversation_id: str | None = None
    customer_id: str | None = None


@dataclass(slots=True)
class RequestOptions:
    params: dict[str, Any] = field(default_factory=dict)
    headers: dict[str, Any] = field(default_factory=dict)
    timeout: float | None = None
    context: GateWayRequestContext | None = None