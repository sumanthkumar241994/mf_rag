from dataclasses import dataclass, field

from app.compliance.response.models.compliance_finding import ComplianceFinding
from app.compliance.response.streaming.processing_request import ProcessingRequest


@dataclass(slots=True)
class StreamState:
    request: ProcessingRequest
    buffer: str = ""
    complete_response: str = ""
    processed_response: str = ""
    findings: list[ComplianceFinding] = field(default_factory=list)
    blocked: bool = False
    reason: str | None = None