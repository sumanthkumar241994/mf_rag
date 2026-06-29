from dataclasses import dataclass

@dataclass(slots=True)
class RequestContext:
    customer_id: str
    session_id: str | None = None