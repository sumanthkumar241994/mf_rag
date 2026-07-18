from abc import ABC
from abc import abstractmethod

from app.compliance.prompt.models.prompt_compliance_request import (
    PromptComplianceRequest,
)
from app.compliance.prompt.models.prompt_compliance_result import (
    PromptComplianceResult,
)


class PromptComplianceValidator(ABC):

    @abstractmethod
    async def validate(
        self,
        request: PromptComplianceRequest,
    ) -> PromptComplianceResult:
        pass