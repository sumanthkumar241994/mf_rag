from app.compliance.enums.compliance_action import ComplianceAction
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


class ContentPolicyValidator(PromptComplianceValidator):

    def __init__(
        self,
        repository: PolicyRepository,
    ):
        self._repository = repository

    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:

        prompt = request.prompt

        text = " ".join(
            filter(
                None,
                (
                    prompt.system_prompt,
                    prompt.user_prompt,
                ),
            )
        )

        for phrase in self._repository.prohibited_phrases.blocked:

            if not phrase.pattern.search(text):
                continue

            if phrase.action == ComplianceAction.REJECT:
                return PromptComplianceResult(
                    allowed=False,
                    sanitized_prompt=prompt,
                    reason=phrase.description,
                )

            # REPLACE is intentionally ignored for prompts.
            # Prompt compliance validates prompts rather than rewriting
            # system or user instructions.
            return PromptComplianceResult(
                allowed=False,
                sanitized_prompt=prompt,
                reason=phrase.description,
            )

        return PromptComplianceResult(
            allowed=True,
            sanitized_prompt=prompt,
        )