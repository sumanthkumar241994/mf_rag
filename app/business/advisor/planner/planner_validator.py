from app.business.advisor.planner.models.planner_error import PlannerError
from app.business.advisor.planner.models.planner_response import PlannerResponse
from app.business.advisor.planner.models.planner_validation_result import (
    PlannerValidationResult,
)


class PlannerValidator:

    def __init__(
        self,
        max_capabilities: int = 5,
    ):
        self._max_capabilities = max_capabilities

    def validate(
        self,
        planner: PlannerResponse,
        
    ) -> PlannerValidationResult:

        errors: list[PlannerError] = []

        self._validate_confidence(planner, errors)
        self._validate_reasons(planner, errors)
        self._validate_duplicates(planner, errors)
        self._validate_capability_limit(planner, errors)

        return PlannerValidationResult(
            valid=len(errors) == 0,
            response=planner if not errors else None,
            errors=errors,
        )

    def _validate_confidence(
        self,
        planner: PlannerResponse,
        errors: list[PlannerError],
    ) -> None:

        confidence = planner.confidence

        if not (0.0 <= confidence <= 1.0):
            errors.append(
                PlannerError(
                    field="confidence",
                    message="Confidence must be between 0.0 and 1.0.",
                )
            )

    def _validate_reasons(
        self,
        planner: PlannerResponse,
        errors: list[PlannerError],
    ) -> None:

        if not planner.reasons:
            errors.append(
                PlannerError(
                    field="reasons",
                    message="At least one capability is required.",
                )
            )
            return

        for index, reason in enumerate(planner.reasons):

            if not reason.reason.strip():
                errors.append(
                    PlannerError(
                        field=f"reasons[{index}].reason",
                        message="Reason cannot be empty.",
                    )
                )

    def _validate_duplicates(
        self,
        planner: PlannerResponse,
        errors: list[PlannerError],
    ) -> None:

        seen = set()

        for reason in planner.reasons:

            if reason.capability in seen:
                errors.append(
                    PlannerError(
                        field="capabilities",
                        message=f"Duplicate capability '{reason.capability.value}'.",
                    )
                )

            seen.add(reason.capability)

    def _validate_capability_limit(
        self,
        planner: PlannerResponse,
        errors: list[PlannerError],
    ) -> None:

        if len(planner.reasons) > self._max_capabilities:
            errors.append(
                PlannerError(
                    field="capabilities",
                    message=(
                        f"Planner selected {len(planner.reasons)} capabilities. "
                        f"Maximum allowed is {self._max_capabilities}."
                    ),
                )
            )