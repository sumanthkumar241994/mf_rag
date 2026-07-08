# from app.business.advisor.enums.tool_type import ToolType
# from app.prompts.templates.advisor.system_prompt import ADVISOR_SYSTEM_PROMPT
# from app.workflows.advisor.advisor_state import AdvisorState
# from app.business.advisor.models.prompt import Prompt


# class AdvisorPromptBuilder:
#     """
#     Builds the final prompt supplied to the LLM.
#     """

#     def build(
#         self,
#         state: AdvisorState,
#     ) -> Prompt:

#         sections: list[str] = []

#         successful_tools = {
#             result["tool"]
#             for result in state.tool_results
#             if result["success"]
#         }

#         # Conversation History
#         if state.history:

#             sections.append("## Conversation History")

#             for message in state.history:
#                 sections.append(
#                     f"{message.role}: {message.content}"
#                 )

#             sections.append("")

#         # Planner
#         if state.planner_result:

#             sections.append("## User Intent")
#             sections.append(state.planner_result.intent.value)

#             sections.append("")

#         # Portfolio Analysis
#         if ToolType.PORTFOLIO in successful_tools and state.portfolio_analysis:

#             sections.append("## Portfolio Analysis")
#             sections.append(str(state.portfolio_analysis))
#             sections.append("")

#         #
#         # Retrieved Context
#         #
#         if state.llm_context:

#             sections.append("## Retrieved Context")
#             sections.append(state.llm_context.context)
#             sections.append("")

#         #
#         # Errors
#         #
#         # if state.errors:

#         #     sections.append("## Notes")

#         #     for error in state.errors:
#         #         sections.append(
#         #             f"- {error.message}"
#         #         )

#         #     sections.append("")

#         #
#         # User Question
#         #
#         sections.append("## User Question")
#         sections.append(state.request.query)

#         return Prompt(
#             system_prompt=ADVISOR_SYSTEM_PROMPT,
#             user_prompt="\n".join(sections),
#         )



from app.business.advisor.models.prompt import Prompt
from app.prompts.builder.advisor.sections.customer_section import CustomerSection
from app.prompts.builder.advisor.sections.portfolio_section import PortfolioSection
from app.prompts.builder.advisor.sections.scheme_section import SchemeSection
from app.prompts.templates.advisor.system_prompt import ADVISOR_SYSTEM_PROMPT
from app.workflows.advisor.advisor_state import AdvisorState


class AdvisorPromptBuilder:
    """
    Builds the final prompt supplied to the LLM.
    """

    def __init__(
        self,
        customer_section: CustomerSection,
        portfolio_section: PortfolioSection,
        scheme_section: SchemeSection,
    ):
        self._customer_section = customer_section
        self._portfolio_section = portfolio_section
        self._scheme_section = scheme_section

    def build(self, state: AdvisorState) -> Prompt:

        sections: list[str] = []

        for section in (
            self._customer_section,
            self._portfolio_section,
            self._scheme_section,
        ):
            sections.extend(section.build(state))

        return Prompt(
            system_prompt=ADVISOR_SYSTEM_PROMPT,
            user_prompt="\n".join(sections),
        )