import json

from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.intent import Intent
from app.business.advisor.planner.exceptions import PlannerParserError
from app.business.advisor.planner.models.planner_reason import PlannerReason
from app.business.advisor.planner.models.planner_response import PlannerResponse


class PlannerParser:

    def parse(self, response: str) -> PlannerResponse:
        try:
            payload = json.loads(response)
        except json.JSONDecodeError as exc:
            raise PlannerParserError(
                "Invalid JSON returned by planner."
            ) from exc

        # Intent
        try:
            intent = Intent(payload["intent"])
        except KeyError as exc:
            raise PlannerParserError(
                "Planner response missing 'intent'."
            ) from exc
        except ValueError as exc:
            raise PlannerParserError(
                f"Unsupported intent '{payload['intent']}'."
            ) from exc

        # Confidence
        try:
            confidence = float(payload["confidence"])
        except KeyError as exc:
            raise PlannerParserError(
                "Planner response missing 'confidence'."
            ) from exc
        except (TypeError, ValueError) as exc:
            raise PlannerParserError(
                "Planner confidence must be a float."
            ) from exc

        # Reasons
        try:
            reason_items = payload["reasons"]
        except KeyError as exc:
            raise PlannerParserError(
                "Planner response missing 'reasons'."
            ) from exc

        if not isinstance(reason_items, list):
            raise PlannerParserError(
                "'reasons' must be a list."
            )

        reasons: list[PlannerReason] = []

        for item in reason_items:

            if not isinstance(item, dict):
                raise PlannerParserError(
                    "Each reason must be an object."
                )

            try:
                capability = Capability(item["capability"])
            except KeyError as exc:
                raise PlannerParserError(
                    "Reason missing 'capability'."
                ) from exc
            except ValueError as exc:
                raise PlannerParserError(
                    f"Unsupported capability '{item['capability']}'."
                ) from exc

            try:
                reason = item["reason"].strip()
            except KeyError as exc:
                raise PlannerParserError(
                    "Reason missing 'reason'."
                ) from exc

            reasons.append(
                PlannerReason(
                    capability=capability,
                    reason=reason,
                )
            )

        return PlannerResponse(
            intent=intent,
            confidence=confidence,
            reasons=reasons,
        )