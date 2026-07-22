from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.langfuse.models.cost import Cost
from app.langfuse.models.usage import Usage


@dataclass(slots=True)
class Observation:
    id: str
    trace_id: str
    type: str
    name: str
    parent_observation_id: str | None
    start_time: datetime
    end_time: datetime | None
    input: Any | None
    output: Any | None
    metadata: dict[str, Any] = field(default_factory=dict)
    model: str | None = None
    usage: Usage | None = None
    cost: Cost | None = None
    usage_details: dict[str, Any] = field(default_factory=dict)
    cost_details: dict[str, Any] = field(default_factory=dict)
    latency: float | None = None