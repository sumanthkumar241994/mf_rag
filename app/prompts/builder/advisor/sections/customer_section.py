from app.business.advisor.enums.tool_type import ToolType
from app.business.customer.models.customer import Customer
from app.prompts.builder.advisor.sections.base_section import BaseSection
from app.workflows.advisor.advisor_state import AdvisorState


class CustomerSection(BaseSection):

    def build(self, state: AdvisorState) -> list[str]:
        if not self.tool_executed(state, ToolType.CUSTOMER):
            return []

        customer = state.customer
        if customer is None:
            return []

        lines: list[str] = []

        self.add_heading(lines, "Customer Information")

        self._add_profile(lines, customer)
        self._add_kyc(lines, customer)
        self._add_bank(lines, customer)
        self._add_investment(lines, customer)
        self._add_nominee(lines, customer)
        self._add_onboarding(lines, customer)
        if customer.knowledge:
            self._add_knowledge(lines, customer)

        return lines

    def _add_profile(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        self.add_heading(prompt, "Profile")

        if customer.profile.age is not None:
            self.add_field(
                prompt,
                "Age",
                customer.profile.age,
            )

        if customer.investment.risk_profile:
            self.add_field(
                prompt,
                "Risk Profile",
                customer.investment.risk_profile,
            )

        self.add_field(
            prompt,
            "Marital Status",
            customer.profile.marital_status.display_name,
        )

        self.add_blank_line(prompt)

    def _add_kyc(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        self.add_heading(prompt, "KYC")

        self.add_field(
            prompt,
            "Status",
            customer.kyc.status.display_name,
        )

        self.add_field(
            prompt,
            "Description",
            customer.kyc.status.description,
        )

        self.add_blank_line(prompt)

    def _add_bank(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        self.add_heading(prompt, "Bank")

        self.add_field(
            prompt,
            "Bank Name",
            customer.bank.bank_name,
        )

        self.add_field(
            prompt,
            "Verified",
            "Yes" if customer.bank.validated else "No",
        )

        self.add_blank_line(prompt)

    def _add_investment(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        self.add_heading(prompt, "Investment")

        self.add_field(
            prompt,
            "Investment Allowed",
            "Yes" if customer.investment.investment_allowed else "No",
        )

        self.add_field(
            prompt,
            "Has Investments",
            "Yes" if customer.investment.has_investments else "No",
        )

        if customer.investment.last_payment_mode:
            self.add_field(
                prompt,
                "Last Payment Mode",
                customer.investment.last_payment_mode,
            )

        self.add_blank_line(prompt)

    def _add_nominee(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        self.add_heading(prompt, "Nominee")

        nominee_added = bool(customer.nominee.name)

        self.add_field(
            prompt,
            "Added",
            "Yes" if nominee_added else "No",
        )

        if nominee_added:
            self.add_field(
                prompt,
                "Relationship",
                customer.nominee.relationship,
            )

        self.add_blank_line(prompt)

    def _add_onboarding(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        self.add_heading(prompt, "Onboarding")

        self.add_field(
            prompt,
            "Status",
            customer.onboarding.status,
        )

        if customer.onboarding.error:
            self.add_field(
                prompt,
                "Error",
                customer.onboarding.error,
            )

        self.add_blank_line(prompt)

    def _add_knowledge(
        self,
        prompt: list[str],
        customer: Customer,
    ) -> None:

        knowledge = customer.knowledge

        has_knowledge = any([
            knowledge.retirement_age.value is not None,
            knowledge.annual_income.value is not None,
            knowledge.monthly_expenses.value is not None,
            knowledge.financial_dependents.value is not None,
            knowledge.investment_horizon.value is not None,
            knowledge.preferred_return_assumption.value is not None,
        ])

        if not has_knowledge:
            return

        self.add_heading(prompt, "Customer Knowledge")

        if knowledge.retirement_age.value is not None:
            self.add_field(
                prompt,
                "Retirement Age",
                knowledge.retirement_age.value,
            )

        if knowledge.annual_income.value is not None:
            self.add_field(
                prompt,
                "Annual Income",
                knowledge.annual_income.value,
            )

        if knowledge.monthly_expenses.value is not None:
            self.add_field(
                prompt,
                "Monthly Expenses",
                knowledge.monthly_expenses.value,
            )

        if knowledge.financial_dependents.value is not None:
            self.add_field(
                prompt,
                "Financial Dependents",
                knowledge.financial_dependents.value,
            )

        if knowledge.investment_horizon.value is not None:
            self.add_field(
                prompt,
                "Investment Horizon (Years)",
                knowledge.investment_horizon.value,
            )

        if knowledge.preferred_return_assumption.value is not None:
            self.add_field(
                prompt,
                "Preferred Return (%)",
                knowledge.preferred_return_assumption.value,
            )

        self.add_blank_line(prompt)