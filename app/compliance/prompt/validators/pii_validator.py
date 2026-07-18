import re
from dataclasses import replace

from app.compliance.prompt.models.pii_finding import PIIFinding
from app.compliance.prompt.models.prompt_compliance_request import (
    PromptComplianceRequest,
)
from app.compliance.prompt.models.prompt_compliance_result import (
    PromptComplianceResult,
)
from app.compliance.prompt.validators.base import (
    PromptComplianceValidator,
)
from app.compliance.repository.policy_repository import (
    PolicyRepository,
)


class PIIValidator(PromptComplianceValidator):
    """
    Detects and masks PII before sending prompts to the LLM.
    """

    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        re.IGNORECASE,
    )

    PHONE_PATTERN = re.compile(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    )

    PAN_PATTERN = re.compile(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        re.IGNORECASE,
    )

    AADHAAR_PATTERN = re.compile(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b"
    )

    CREDIT_CARD_PATTERN = re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    )

    def __init__(
        self,
        repository: PolicyRepository,
    ):
        self._repository = repository

    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:

        findings: list[PIIFinding] = []

        sanitized = replace(request.prompt)

        sanitized.system_prompt = self._mask(
            sanitized.system_prompt,
            findings,
        )

        sanitized.user_prompt = self._mask(
            sanitized.user_prompt,
            findings,
        )


        return PromptComplianceResult(
            allowed=True,
            sanitized_prompt=sanitized,
            findings=findings,
        )

    def _mask(
        self,
        text: str | None,
        findings: list[PIIFinding],
    ) -> str | None:

        if text is None:
            return None

        replacements = [
            (
                self.EMAIL_PATTERN,
                "EMAIL",
            ),
            (
                self.PHONE_PATTERN,
                "PHONE",
            ),
            (
                self.PAN_PATTERN,
                "PAN",
            ),
            (
                self.AADHAAR_PATTERN,
                "AADHAAR",
            ),
            (
                self.CREDIT_CARD_PATTERN,
                "CREDIT_CARD",
            ),
        ]

        for pattern, pii_type in replacements:

            def replacer(match: re.Match) -> str:

                findings.append(
                    PIIFinding(
                        type=pii_type,
                        value=match.group(0),
                        replacement=f"[{pii_type}]",
                    )
                )

                return f"[{pii_type}]"

            text = pattern.sub(
                replacer,
                text,
            )

        return text