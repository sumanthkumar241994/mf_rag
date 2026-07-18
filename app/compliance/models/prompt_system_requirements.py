from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PromptSystemRequirements:
    use_retrieved_context_only: bool
    never_fabricate_information: bool
    admit_when_information_is_missing: bool
    never_reveal_system_prompt: bool
    never_reveal_internal_context: bool
    never_expose_customer_pii: bool
    never_claim_regulatory_approval: bool
    no_guaranteed_returns: bool
    no_personalized_investment_advice_without_disclaimer: bool
    require_human_review_for_high_risk_actions: bool