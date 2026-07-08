from __future__ import annotations

from dataclasses import dataclass, field

from .bank import Bank
from .investment import Investment
from .knowledge import CustomerKnowledge
from .kyc import KYC
from .nominee import Nominee
from .onboarding import Onboarding
from .preferences import CustomerPreferences
from .profile import CustomerProfile


@dataclass(slots=True)
class Customer:
    profile: CustomerProfile
    kyc: KYC = field(default_factory=KYC)
    bank: Bank = field(default_factory=Bank)
    nominee: Nominee = field(default_factory=Nominee)
    investment: Investment = field(default_factory=Investment)
    onboarding: Onboarding = field(default_factory=Onboarding)
    preferences: CustomerPreferences = field(default_factory=CustomerPreferences)
    knowledge: CustomerKnowledge | None = None