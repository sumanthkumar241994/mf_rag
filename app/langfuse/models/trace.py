from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.langfuse.models.observation import Observation


@dataclass(slots=True)
class Trace:
    id: str
    name: str
    timestamp: datetime
    input: Any | None
    output: Any | None
    metadata: dict[str, Any] = field(default_factory=dict)
    latency: float | None = None
    total_cost: float | None = None
    observations: list[Observation] = field(default_factory=list)