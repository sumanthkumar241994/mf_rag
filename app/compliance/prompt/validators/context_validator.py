from app.compliance.prompt.models.prompt_compliance_request import (
    PromptComplianceRequest,
)
from app.compliance.prompt.models.prompt_compliance_result import (
    PromptComplianceResult,
)
from app.compliance.prompt.validators.base import (
    PromptComplianceValidator,
)


class ContextValidator(PromptComplianceValidator):

    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:

        if (
            request.prompt.user_prompt is None
            or not request.prompt.user_prompt.strip()
        ):
            return PromptComplianceResult(
                allowed=False,
                sanitized_prompt=request.prompt,
                reason="Prompt context is required.",
            )

        return PromptComplianceResult(
            allowed=True,
            sanitized_prompt=request.prompt,
        )