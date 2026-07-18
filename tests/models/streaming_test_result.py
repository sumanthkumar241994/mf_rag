from dataclasses import dataclass

from app.compliance.response.streaming.stream_state import StreamState



@dataclass(slots=True, frozen=True)
class StreamingTestResult:
    output: str
    state: StreamState