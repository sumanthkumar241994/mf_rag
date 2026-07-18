import re

from app.compliance.enums.compliance_action import ComplianceAction
from app.compliance.enums.compliance_finding_type import ComplianceFindingType
from app.compliance.response.models.compliance_finding import ComplianceFinding
from app.compliance.response.streaming.processing_request import (
    ProcessingRequest,
)
from app.compliance.response.streaming.processing_result import (
    ProcessingResult,
)
from app.compliance.response.validators.base import (
    ResponseComplianceValidator,
)
from app.compliance.repository.policy_repository import (
    PolicyRepository,
)


class PolicyValidator(ResponseComplianceValidator):

    def __init__(
        self,
        repository: PolicyRepository,
    ) -> None:
        self._repository = repository

    async def process(
        self,
        request: ProcessingRequest,
    ) -> ProcessingResult:

        text = request.text
        findings: list[ComplianceFinding] = []

        for phrase in self._repository.prohibited_phrases.blocked:

            if not phrase.pattern.search(text):
                continue

            findings.append(
                ComplianceFinding(
                    type=ComplianceFindingType.POLICY,
                    description=phrase.description,
                    severity=phrase.severity,
                )
            )

            if phrase.action == ComplianceAction.REJECT:
                return ProcessingResult.failure(
                    request=request,
                    reason=phrase.description,
                    findings=findings,
                )

            if (
                phrase.action == ComplianceAction.REPLACE
                and phrase.replacement
            ):
                text = phrase.pattern.sub(
                    phrase.replacement,
                    text,
                )

        return ProcessingResult.success(
            request=request.with_text(text),
            findings=findings,
        )