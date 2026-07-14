from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.goal_projection import GoalProjection


class GoalCalculator:
    MONTHS_IN_YEAR = Decimal("12")
    HUNDRED = Decimal("100")
    ZERO = Decimal("0")
    ONE = Decimal("1")

    def calculate(self, parameters: GoalParameters) -> GoalProjection:
        self._validate(parameters)

        months = parameters.target_years * 12

        monthly_return = (
            parameters.expected_return
            / self.HUNDRED
            / self.MONTHS_IN_YEAR
        )

        monthly_inflation = (
            parameters.inflation_rate
            / self.HUNDRED
            / self.MONTHS_IN_YEAR
        )

        future_goal_amount = self._future_goal_amount(
            goal_amount=parameters.goal_amount,
            monthly_inflation=monthly_inflation,
            months=months,
        )

        future_value_of_corpus = self._future_value(
            principal=parameters.current_corpus,
            monthly_rate=monthly_return,
            months=months,
        )

        future_value_of_existing_sip = self._future_value_of_sip(
            monthly_investment=parameters.monthly_investment,
            monthly_rate=monthly_return,
            months=months,
        )

        projected_corpus = (
            future_value_of_corpus
            + future_value_of_existing_sip
        )

        funding_gap = max(
            self.ZERO,
            future_goal_amount - projected_corpus,
        )

        required_monthly_investment = self._required_monthly_investment(
            goal_amount=future_goal_amount,
            current_corpus=parameters.current_corpus,
            monthly_rate=monthly_return,
            months=months,
        )

        additional_monthly_investment = max(
            self.ZERO,
            required_monthly_investment - parameters.monthly_investment,
        )

        return GoalProjection(
            projected_goal_amount=self._round(future_goal_amount),
            projected_corpus=self._round(projected_corpus),
            funding_gap=self._round(funding_gap),
            required_monthly_investment=self._round(
                required_monthly_investment
            ),
            additional_monthly_investment=self._round(
                additional_monthly_investment
            ),
        )

    def _future_goal_amount(
        self,
        goal_amount: Decimal,
        monthly_inflation: Decimal,
        months: int,
    ) -> Decimal:

        return goal_amount * (
            (self.ONE + monthly_inflation) ** months
        )

    def _future_value(
        self,
        principal: Decimal,
        monthly_rate: Decimal,
        months: int,
    ) -> Decimal:

        if principal <= self.ZERO:
            return self.ZERO

        return principal * (
            (self.ONE + monthly_rate) ** months
        )

    def _future_value_of_sip(
        self,
        monthly_investment: Decimal,
        monthly_rate: Decimal,
        months: int,
    ) -> Decimal:

        if monthly_investment <= self.ZERO:
            return self.ZERO

        if monthly_rate == self.ZERO:
            return monthly_investment * Decimal(months)

        growth = (self.ONE + monthly_rate) ** months

        return (
            monthly_investment
            * ((growth - self.ONE) / monthly_rate)
            * (self.ONE + monthly_rate)
        )

    def _required_monthly_investment(
        self,
        goal_amount: Decimal,
        current_corpus: Decimal,
        monthly_rate: Decimal,
        months: int,
    ) -> Decimal:

        future_value_of_corpus = self._future_value(
            principal=current_corpus,
            monthly_rate=monthly_rate,
            months=months,
        )

        remaining_amount = max(
            self.ZERO,
            goal_amount - future_value_of_corpus,
        )

        if remaining_amount == self.ZERO:
            return self.ZERO

        if monthly_rate == self.ZERO:
            return remaining_amount / Decimal(months)

        growth = (self.ONE + monthly_rate) ** months

        factor = (
            ((growth - self.ONE) / monthly_rate)
            * (self.ONE + monthly_rate)
        )

        return remaining_amount / factor

    @staticmethod
    def _round(
        value: Decimal,
    ) -> Decimal:
        return value.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @staticmethod
    def _validate(parameters: GoalParameters) -> None:

        required = {
            "goal_amount": parameters.goal_amount,
            "target_years": parameters.target_years,
            "current_corpus": parameters.current_corpus,
            "monthly_investment": parameters.monthly_investment,
            "expected_return": parameters.expected_return,
            "inflation_rate": parameters.inflation_rate,
        }

        missing = [
            name
            for name, value in required.items()
            if value is None
        ]

        if missing:
            raise ValueError(
                f"Missing goal parameters: {', '.join(missing)}"
            )