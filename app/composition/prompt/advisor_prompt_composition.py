from app.prompts.builder.advisor.advisor_prompt_builder import AdvisorPromptBuilder
from app.prompts.builder.advisor.sections.customer_section import CustomerSection
from app.prompts.builder.advisor.sections.portfolio_section import PortfolioSection
from app.prompts.builder.advisor.sections.scheme_section import SchemeSection


class AdvisorPromptComposition:
    def __init__(self) -> None:
        self.prompt_builder = AdvisorPromptBuilder(
            customer_section=CustomerSection(),
            portfolio_section=PortfolioSection(),
            scheme_section=SchemeSection()
        )