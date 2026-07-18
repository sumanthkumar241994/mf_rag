from dataclasses import dataclass

from app.compliance.models.prompt_limits import PromptLimits
from app.compliance.models.prompt_system_requirements import PromptSystemRequirements


@dataclass(slots=True)
class PromptPolicy:
    system_requirements: PromptSystemRequirements
    limits: PromptLimits