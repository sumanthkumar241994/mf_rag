from dataclasses import dataclass, field

from app.compliance.prompt.models.pii_finding import PIIFinding
from app.compliance.prompt.models.sanitzed_prompt import SanitizedPrompt


@dataclass(slots=True)
class PromptComplianceResult:
    allowed: bool
    sanitized_prompt: SanitizedPrompt
    findings: list[PIIFinding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    reason: str | None = None