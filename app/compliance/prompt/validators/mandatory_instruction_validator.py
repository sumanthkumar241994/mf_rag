from app.compliance.prompt.models.prompt_compliance_request import PromptComplianceRequest
from app.compliance.prompt.models.prompt_compliance_result import PromptComplianceResult
from app.compliance.prompt.models.sanitzed_prompt import SanitizedPrompt
from app.compliance.prompt.validators.base import PromptComplianceValidator
from app.compliance.repository.policy_repository import PolicyRepository


class MandatoryInstructionValidator(PromptComplianceValidator):

    def __init__(
        self,
        repository: PolicyRepository,
    ):
        self._repository = repository

    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:

        system_prompt = request.prompt.system_prompt or ""

        # TODO: Read from PromptPolicy instead of hardcoding
        required = [
            "retrieved context",
            "never fabricate",
            "admit when information is unavailable",
        ]

        for instruction in required:
            if instruction.lower() not in system_prompt.lower():
                return PromptComplianceResult(
                    allowed=False,
                    sanitized_prompt=SanitizedPrompt(
                        system_prompt=request.prompt.system_prompt,
                        user_prompt=request.prompt.user_prompt,
                    ),
                    reason=f"Missing mandatory instruction: {instruction}",
                )

        return PromptComplianceResult(
            allowed=True,
            sanitized_prompt=SanitizedPrompt(
                system_prompt=request.prompt.system_prompt,
                user_prompt=request.prompt.user_prompt,
            ),
        )