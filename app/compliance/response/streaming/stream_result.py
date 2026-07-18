from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StreamResult:
    """
    Result returned by a streaming validator.
    """
    chunk: str
    processed_response: str = ""
    completed: bool = False
    blocked: bool = False
    reason: str | None = None