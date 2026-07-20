from dataclasses import replace

from app.compliance.prompt.models.prompt_compliance_request import (
    PromptComplianceRequest,
)
from app.compliance.prompt.models.prompt_compliance_result import (
    PromptComplianceResult,
)
from app.compliance.prompt.validators.base import (
    PromptComplianceValidator,
)
from app.observability.tracing import trace_step


class PromptComplianceService:

    def __init__(
        self,
        validators: list[PromptComplianceValidator],
    ):
        self._validators = validators

    @trace_step(
        "prompt_compliance",
        output_mapper=lambda result: {
            "allowed": result.allowed,
            "findings": len(result.findings),
            "santized_promt": result.sanitized_prompt
        }
    )
    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:

        findings = []
        warnings = []

        current_request = request

        for validator in self._validators:

            result = await validator.validate(current_request)

            findings.extend(result.findings)
            warnings.extend(result.warnings)

            if not result.allowed:
                result.findings = findings
                result.warnings = warnings
                return result

            current_request = replace(
                current_request,
                prompt=result.sanitized_prompt,
            )

        return PromptComplianceResult(
            allowed=True,
            sanitized_prompt=current_request.prompt,
            findings=findings,
            warnings=warnings,
        )