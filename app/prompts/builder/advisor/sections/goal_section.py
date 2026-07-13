from app.business.advisor.enums.tool_type import ToolType
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.prompts.builder.advisor.sections.base_section import BaseSection
from app.workflows.advisor.advisor_state import AdvisorState


class GoalSection(BaseSection):

    def build(
        self,
        state: AdvisorState,
    ) -> list[str]:

        if not self.tool_executed(state, ToolType.GOAL):
            return []
        print(type(state))
        analysis = state.goal_analysis

        if analysis is None:
            return []

        lines: list[str] = []

        self.add_heading(lines, "Goal Planning")

        self._add_goal(lines, analysis)
        self._add_inputs(lines, analysis)
        self._add_projection(lines, analysis)
        self._add_insights(lines, analysis)
        self._add_recommendations(lines, analysis)

        return lines

    def _add_goal(
        self,
        prompt: list[str],
        analysis: GoalAnalysis,
    ) -> None:

        self.add_heading(prompt, "Goal")

        self.add_field(
            prompt,
            "Type",
            analysis.goal.title,
        )

        self.add_field(
            prompt,
            "Status",
            analysis.status.value if analysis.status else "Unknown",
        )

        self.add_blank_line(prompt)

    def _add_inputs(
        self,
        prompt: list[str],
        analysis: GoalAnalysis,
    ) -> None:

        parameters = analysis.parameters

        self.add_heading(prompt, "Inputs")

        self.add_field(
            prompt,
            "Current Age",
            parameters.current_age,
        )

        self.add_field(
            prompt,
            "Retirement Age",
            parameters.retirement_age,
        )

        self.add_field(
            prompt,
            "Target Years",
            parameters.target_years,
        )

        self.add_field(
            prompt,
            "Target Corpus",
            parameters.goal_amount,
        )

        self.add_field(
            prompt,
            "Current Corpus",
            parameters.current_corpus,
        )

        self.add_field(
            prompt,
            "Monthly Investment",
            parameters.monthly_investment,
        )

        self.add_field(
            prompt,
            "Expected Return (%)",
            parameters.expected_return,
        )

        self.add_field(
            prompt,
            "Inflation Rate (%)",
            parameters.inflation_rate,
        )

        self.add_blank_line(prompt)

    def _add_projection(
        self,
        prompt: list[str],
        analysis: GoalAnalysis,
    ) -> None:

        if analysis.projection is None:
            return

        projection = analysis.projection

        self.add_heading(prompt, "Projection")

        self.add_field(
            prompt,
            "Inflation Adjusted Goal",
            projection.projected_goal_amount,
        )

        self.add_field(
            prompt,
            "Projected Corpus",
            projection.projected_corpus,
        )

        self.add_field(
            prompt,
            "Funding Gap",
            projection.funding_gap,
        )

        self.add_field(
            prompt,
            "Required Monthly Investment",
            projection.required_monthly_investment,
        )

        self.add_blank_line(prompt)

    def _add_insights(
        self,
        prompt: list[str],
        analysis: GoalAnalysis,
    ) -> None:

        if not analysis.insights:
            return

        self.add_heading(prompt, "Insights")

        for insight in analysis.insights:
            prompt.append(
                f"- {insight.title}: {insight.description}"
            )

        self.add_blank_line(prompt)

    def _add_recommendations(
        self,
        prompt: list[str],
        analysis: GoalAnalysis,
    ) -> None:

        if not analysis.recommendations:
            return

        self.add_heading(prompt, "Recommendations")

        for recommendation in analysis.recommendations:
            prompt.append(
                f"- {recommendation.title}: {recommendation.description}"
            )

        self.add_blank_line(prompt)