from app.business.customer.enums.kyc_status import KYCStatus
from app.investment.base.models import InvestmentBaseModel
from app.investment.business.customer.enums.onboarding_status import OnboardingStatus
from app.investment.business.customer.enums.signature_status import SignatureStatus


class OnboardingDetails(InvestmentBaseModel):
    ok_for_investment: bool = False

    bank_updated: bool = False
    bank_validated: bool = False

    fatca_updated: bool = False

    kyc_verified: bool = False

    address_updated: bool = False

    email_verified: bool = False

    mobile_verified: bool = False

    signature_status: SignatureStatus | None = None

    onboarding_status: OnboardingStatus | None = None

    kyc_status: KYCStatus | None = None