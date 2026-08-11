from app.business.customer.enums.kyc_status import KYCStatus
from app.investment.business.customer.models.customer import Customer
from app.investment.common.enums.eligibility_requirement_type import (
    EligibilityRequirementType,
)
from app.investment.common.enums.requirement_status import (
    RequirementStatus,
)
from app.investment.models.eligibility import Eligibility
from app.investment.models.eligibility_requirement import (
    EligibilityRequirement,
)


class EligibilityService:

    def evaluate(
        self,
        customer: Customer,
    ) -> Eligibility:

        if customer.onboarding_details.ok_for_investment:
            return Eligibility(
                eligible=True,
            )

        eligibility = Eligibility()

        self._evaluate_bank(
            customer,
            eligibility,
        )

        self._evaluate_nominee(
            customer,
            eligibility,
        )

        self._evaluate_fatca(
            customer,
            eligibility,
        )

        self._evaluate_kyc(
            customer,
            eligibility,
        )

        self._evaluate_signature(
            customer,
            eligibility,
        )

        eligibility.eligible = (
            not eligibility.required
            and not eligibility.pending
        )

        return eligibility

    def _evaluate_bank(
        self,
        customer: Customer,
        eligibility: Eligibility,
    ) -> None:

        if not customer.bank.updated:
            eligibility.required.append(
                EligibilityRequirement(
                    code=EligibilityRequirementType.BANK,
                    status=RequirementStatus.REQUIRED,
                    title="Bank Details",
                    message="Please add your bank account.",
                )
            )
            return

        if not customer.bank.validated:
            eligibility.pending.append(
                EligibilityRequirement(
                    code=EligibilityRequirementType.BANK,
                    status=RequirementStatus.PENDING,
                    title="Bank Verification",
                    message="Your bank account verification is in progress.",
                )
            )

    def _evaluate_nominee(
        self,
        customer: Customer,
        eligibility: Eligibility,
    ) -> None:

        if customer.nominee.is_complete:
            return

        eligibility.required.append(
            EligibilityRequirement(
                code=EligibilityRequirementType.NOMINEE,
                status=RequirementStatus.REQUIRED,
                title="Nominee Details",
                message="Please complete your nominee details.",
            )
        )

    def _evaluate_fatca(
        self,
        customer: Customer,
        eligibility: Eligibility,
    ) -> None:

        if customer.onboarding_details.fatca_updated:
            return

        eligibility.required.append(
            EligibilityRequirement(
                code=EligibilityRequirementType.FATCA,
                status=RequirementStatus.REQUIRED,
                title="FATCA Declaration",
                message="Please complete your FATCA declaration.",
            )
        )

    def _evaluate_kyc(
        self,
        customer: Customer,
        eligibility: Eligibility,
    ) -> None:

        kyc = customer.kyc

        if kyc.can_invest:
            return

        requirement = EligibilityRequirement(
            code=EligibilityRequirementType.KYC,
            title="KYC Required",
            message="Please complete your KYC",
            status=(
                RequirementStatus.PENDING
                if kyc.status == KYCStatus.SUBMITTED
                else RequirementStatus.REQUIRED
            ),
        )

        if requirement.status == RequirementStatus.PENDING:
            eligibility.pending.append(requirement)
        else:
            eligibility.required.append(requirement)

    def _evaluate_signature(
        self,
        customer: Customer,
        eligibility: Eligibility,
    ) -> None:

        status = customer.onboarding_details.signature_status

        if status.is_completed:
            return

        requirement = EligibilityRequirement(
            code=EligibilityRequirementType.SIGNATURE,
            title="Signature",
            message="Signature uploaded",
            status=(
                RequirementStatus.PENDING
                if status.is_pending
                else RequirementStatus.REQUIRED
            ),
        )

        if requirement.status == RequirementStatus.PENDING:
            eligibility.pending.append(requirement)
        else:
            eligibility.required.append(requirement)