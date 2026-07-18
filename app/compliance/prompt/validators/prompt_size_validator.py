from app.compliance.prompt.models.prompt_compliance_request import (
    PromptComplianceRequest,
)
from app.compliance.prompt.models.prompt_compliance_result import (
    PromptComplianceResult,
)
from app.compliance.prompt.validators.base import (
    PromptComplianceValidator,
)


class PromptSizeValidator(PromptComplianceValidator):
    """
    Validates that the prompt contains meaningful content.

    Note:
        Model-specific token limits are enforced by the LLM Gateway.
    """

    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:

        prompt = request.prompt

        has_content = any(
            (
                prompt.system_prompt and prompt.system_prompt.strip(),
                prompt.user_prompt and prompt.user_prompt.strip(),
            )
        )

        if not has_content:
            return PromptComplianceResult(
                allowed=False,
                sanitized_prompt=prompt,
                reason="Prompt is empty.",
            )

        return PromptComplianceResult(
            allowed=True,
            sanitized_prompt=prompt,
        )