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
from app.observability.tracing import trace_step
from app.prompts.builder.advisor.sections.document_section import DocumentSection
from app.prompts.builder.advisor.sections.customer_section import CustomerSection
from app.prompts.builder.advisor.sections.goal_section import GoalSection
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
        goal_section: GoalSection,
        document_section: DocumentSection
    ):
        self._customer_section = customer_section
        self._portfolio_section = portfolio_section
        self._scheme_section = scheme_section
        self._goal_section = goal_section
        self._document_section = document_section


    @trace_step(
        "prompt_builder",
        input_mapper=lambda self, state: {
            "has_customer": state.customer is not None,
            "has_portfolio": state.portfolio_analysis is not None,
            "has_goal": state.goal_analysis is not None,
            "has_schemes": bool(state.schemes),
            "has_documents": state.llm_context is not None,
            "history_messages": len(state.history)
        },
        output_mapper=lambda prompt: {
            "system_prompt_length": len(prompt.system_prompt),
            "user_prompt_length": len(prompt.user_prompt),
            "total_prompt_length": (
                len(prompt.system_prompt) + len(prompt.user_prompt)
            ),
        },
    )
    def build(self, state: AdvisorState) -> Prompt:

        sections: list[str] = []

        for section in (
            self._customer_section,
            self._portfolio_section,
            self._scheme_section,
            self._goal_section,
            self._document_section
        ):
            sections.extend(section.build(state))

        return Prompt(
            system_prompt=ADVISOR_SYSTEM_PROMPT,
            user_prompt="\n".join(sections),
        )