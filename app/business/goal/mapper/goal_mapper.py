from app.business.goal.enums.goal_status import GoalStatus
from app.business.goal.models.goal import Goal
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.goal_projection import GoalProjection
from app.business.goal.models.parameter_resolution import ParameterResolution
from app.business.portfolio.analysis.models.insight import Insight
from app.business.portfolio.analysis.models.recommendation import Recommendation


class GoalMapper:

    @staticmethod
    def from_dict(data: dict | GoalAnalysis) -> GoalAnalysis:
        if isinstance(data, GoalAnalysis):
            return data

        status = data.get("status")
        
        return GoalAnalysis(
            goal=GoalMapper._goal(data["goal"]),
            parameters=GoalMapper._parameters(data["parameters"]),
            parameter_resolution=GoalMapper._parameter_resolution(
                data["parameter_resolution"]
            ),
            projection=GoalMapper._projection(
                data.get("projection")
            ),
            insights=[
                GoalMapper._insight(item)
                for item in data.get("insights", [])
            ],
            recommendations=[
                GoalMapper._recommendation(item)
                for item in data.get("recommendations", [])
            ],
            status=(
                status
                if isinstance(status, GoalStatus)
                else GoalStatus(status)
                if status is not None
                else None
    )
        )

    @staticmethod
    def _goal(data: dict | Goal) -> Goal:
        if isinstance(data, Goal):
            return data

        return Goal(**data)

    @staticmethod
    def _parameters(
        data: dict | GoalParameters,
    ) -> GoalParameters:
        if isinstance(data, GoalParameters):
            return data

        return GoalParameters(**data)

    @staticmethod
    def _parameter_resolution(
        data: dict | ParameterResolution,
    ) -> ParameterResolution:
        if isinstance(data, ParameterResolution):
            return data

        return ParameterResolution(**data)

    @staticmethod
    def _projection(
        data: dict | GoalProjection | None,
    ) -> GoalProjection | None:
        if data is None:
            return None

        if isinstance(data, GoalProjection):
            return data

        return GoalProjection(**data)

    @staticmethod
    def _insight(
        data: dict | Insight,
    ) -> Insight:
        if isinstance(data, Insight):
            return data

        return Insight(**data)

    @staticmethod
    def _recommendation(
        data: dict | Recommendation,
    ) -> Recommendation:
        if isinstance(data, Recommendation):
            return data

        return Recommendation(**data)