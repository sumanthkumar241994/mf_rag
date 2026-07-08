from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.business.customer.enums.nominee_identity_type import NomineeIdentityType


@dataclass(slots=True)
class Nominee:
    exists: bool = False
    name: str | None = None
    relationship: str | None = None
    date_of_birth: date | None = None
    guardian: str | None = None
    identity_type: NomineeIdentityType = NomineeIdentityType.UNKNOWN