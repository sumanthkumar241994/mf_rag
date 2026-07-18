from dataclasses import dataclass, field

from app.compliance.response.models.compliance_finding import ComplianceFinding
from app.compliance.response.streaming.processing_request import ProcessingRequest


@dataclass(slots=True)
class ProcessingResult:

    request: ProcessingRequest

    findings: list[ComplianceFinding] = field(
        default_factory=list,
    )

    blocked: bool = False

    reason: str | None = None

    @classmethod
    def success(
        cls,
        request: ProcessingRequest,
        findings: list[ComplianceFinding] | None = None,
    ) -> "ProcessingResult":
        return cls(
            request=request,
            findings=findings or [],
        )


    @classmethod
    def failure(
        cls,
        request: ProcessingRequest,
        reason: str,
        findings: list[ComplianceFinding],
    ) -> "ProcessingResult":
        return cls(
            request=request,
            findings=findings,
            blocked=True,
            reason=reason,
        )