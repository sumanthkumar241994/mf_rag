from app.compliance.prompt.prompt_compliance_service import PromptComplianceService
from app.compliance.prompt.validators.content_policy_validator import ContentPolicyValidator
from app.compliance.prompt.validators.context_validator import (
    ContextValidator,
)
from app.compliance.prompt.validators.mandatory_instruction_validator import (
    MandatoryInstructionValidator,
)
from app.compliance.prompt.validators.pii_validator import (
    PIIValidator,
)
from app.compliance.prompt.validators.prompt_size_validator import PromptSizeValidator
from app.compliance.repository.policy_repository import (
    PolicyRepository,
)
from app.workflows.advisor.nodes.prompt_compliance_node import PromptComplianceNode


class PromptComplianceComposition:

    def __init__(
        self,
        policy_repository: PolicyRepository,
    ):

        validators = [
            MandatoryInstructionValidator(
                repository=policy_repository,
            ),
            ContextValidator(),
            # PromptSizeValidator(),
            ContentPolicyValidator(
                repository=policy_repository,
            ),
            PIIValidator(
                repository=policy_repository,
            ),
        ]

        self.service = PromptComplianceService(
            validators=validators,
        )