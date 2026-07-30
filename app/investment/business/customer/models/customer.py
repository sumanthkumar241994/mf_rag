from pydantic import Field

from app.investment.base.models import InvestmentBaseModel
from .bank import Bank
from .investment import Investment
from .knowledge import CustomerKnowledge
from .kyc import KYC
from .nominee import Nominee
from .onboarding import Onboarding
from .preferences import CustomerPreferences
from .profile import CustomerProfile


class Customer(InvestmentBaseModel):
    profile: CustomerProfile
    kyc: KYC = Field(default_factory=KYC)
    bank: Bank = Field(default_factory=Bank)
    nominee: Nominee = Field(default_factory=Nominee)
    investment: Investment = Field(default_factory=Investment)
    onboarding: Onboarding = Field(default_factory=Onboarding)
    preferences: CustomerPreferences = Field(default_factory=CustomerPreferences)
    knowledge: CustomerKnowledge | None = None