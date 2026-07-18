from dataclasses import dataclass

from app.compliance.models.prompt_policy import PromptPolicy
from app.compliance.models.response_policy import ResponsePolicy
from app.compliance.models.prohibited_phrases import ProhibitedPhrases
from app.compliance.models.regulatory_links import RegulatoryLinks


@dataclass(slots=True, frozen=True)
class CompliancePolicies:
    prompt: PromptPolicy
    prohibited_phrases: ProhibitedPhrases
    regulatory_links: RegulatoryLinks