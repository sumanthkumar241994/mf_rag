from __future__ import annotations

from datetime import date

from pydantic import Field

from app.investment.base.models import InvestmentBaseModel
from app.investment.business.customer.enums.nominee_field import NomineeField
from app.investment.business.customer.enums.nominee_identity_type import (
    NomineeIdentityType,
)


class Nominee(InvestmentBaseModel):
    exists: bool = False

    name: str | None = None
    relationship: str | None = None
    date_of_birth: date | None = None

    guardian: str | None = None

    identity_type: NomineeIdentityType | None = None
    identity_number: str | None = None

    email: str | None = None
    mobile: str | None = None

    @property
    def age(self) -> int | None:
        if self.date_of_birth is None:
            return None

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (
                    self.date_of_birth.month,
                    self.date_of_birth.day,
                )
            )
        )

    @property
    def is_minor(self) -> bool:
        age = self.age

        return age is not None and age < 18

    @property
    def is_complete(self) -> bool:
        """
        Returns True when nominee details are sufficient
        for investment onboarding.
        """

        if not self.exists:
            return False

        required_fields = [
            self.name,
            self.relationship,
            self.date_of_birth,
            self.identity_type,
            self.identity_number,
            self.email,
            self.mobile,
        ]

        if any(
            value in (None, "")
            for value in required_fields
        ):
            return False

        # Minor nominee requires guardian
        if self.is_minor:
            if not self.guardian:
                return False

        return True
    
    @property
    def missing_fields(self) -> list[NomineeField]:

        missing: list[NomineeField] = []

        if not self.exists:
            return [
                NomineeField.NAME,
                NomineeField.RELATIONSHIP,
                NomineeField.DATE_OF_BIRTH,
                NomineeField.IDENTITY_TYPE,
                NomineeField.IDENTITY_NUMBER,
                NomineeField.EMAIL,
                NomineeField.MOBILE,
            ]

        if not self.name:
            missing.append(NomineeField.NAME)

        if not self.relationship:
            missing.append(NomineeField.RELATIONSHIP)

        if self.date_of_birth is None:
            missing.append(NomineeField.DATE_OF_BIRTH)

        if self.identity_type is None:
            missing.append(NomineeField.IDENTITY_TYPE)

        if not self.identity_number:
            missing.append(NomineeField.IDENTITY_NUMBER)

        if not self.email:
            missing.append(NomineeField.EMAIL)

        if not self.mobile:
            missing.append(NomineeField.MOBILE)

        if self.is_minor and not self.guardian:
            missing.append(NomineeField.GUARDIAN)

        return missing