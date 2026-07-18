from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.models.prohibited_phrases import ProhibitedPhrases
from app.compliance.models.prompt_policy import PromptPolicy
from app.compliance.models.regulatory_links import RegulatoryLinks
from app.compliance.models.response_policy import ResponsePolicy


class PolicyRepository:

    def __init__(
        self,
        loader: PolicyLoader,
    ):
        self._policies = loader.load()

    @property
    def prompt_policy(self) -> PromptPolicy:
        return self._policies.prompt

    # @property
    # def response_policy(self) -> ResponsePolicy:
    #     return self._policies.response

    @property
    def prohibited_phrases(self) -> ProhibitedPhrases:
        return self._policies.prohibited_phrases

    @property
    def regulatory_links(self) -> RegulatoryLinks:
        return self._policies.regulatory_links