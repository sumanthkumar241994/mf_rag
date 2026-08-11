from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from app.investment.business.customer.enums.address_type import AddressType
from app.investment.business.customer.enums.annual_income_code import AnnualIncomeCode
from app.investment.business.customer.enums.gender import Gender
from app.investment.business.customer.enums.kyc_status import KYCStatus
from app.investment.business.customer.enums.marital_status import MaritalStatus
from app.investment.business.customer.enums.nominee_identity_type import NomineeIdentityType
from app.investment.business.customer.enums.occupation_code import OccupationCode
from app.investment.business.customer.enums.onboarding_status import OnboardingStatus
from app.investment.business.customer.enums.signature_status import SignatureStatus
from app.investment.business.customer.enums.source_of_wealth_code import SourceOfWealthCode
from app.investment.business.customer.models.bank import Bank
from app.investment.business.customer.models.customer import Customer
from app.investment.business.customer.models.fatca import Fatca
from app.investment.business.customer.models.investment import Investment
from app.investment.business.customer.models.kyc import KYC
from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.customer.models.onboarding import Onboarding
from app.investment.business.customer.models.onboarding_details import OnboardingDetails
from app.investment.business.customer.models.preferences import CustomerPreferences
from app.investment.business.customer.models.profile import CustomerProfile



class CustomerMapper:

    @staticmethod
    def map(data: dict) -> Customer:
        return Customer(
            profile=CustomerMapper._map_profile(data),
            kyc=CustomerMapper._map_kyc(data),
            bank=CustomerMapper._map_bank(data),
            nominee=CustomerMapper._map_nominee(
                data.get("nominee_details")
            ),
            fatca=CustomerMapper._map_fatca(data),
            investment=CustomerMapper._map_investment(data),
            onboarding=CustomerMapper._map_onboarding(data),
            onboarding_details=CustomerMapper._map_onboarding_details(data),
            preferences=CustomerMapper._map_preferences(
                data.get("settings")
            ),
            knowledge=None,
        )

    @staticmethod
    def _map_fatca(
    data: dict,
    ) -> Fatca:

        if not data:
            return Fatca()

        return Fatca(
            occupation_code=(
                OccupationCode(data["occupation_code"])
                if data.get("occupation_code")
                else None
            ),
            annual_income_code=(
                AnnualIncomeCode(data["annual_income_code"])
                if data.get("annual_income_code")
                else None
            ),
            source_of_wealth_code=(
                SourceOfWealthCode(data["source_of_wealth_code"])
                if data.get("source_of_wealth_code")
                else None
            ),
            birth_country=data.get(
                "birth_country",
                "IN",
            ),
            address_type=(
                AddressType.from_api(data["address_type"])
                if data.get("address_type")
                else None
            ),
            is_indian_tax_payer=data.get(
                "is_indian_tax_payer",
            ),
            politically_exposed=data.get(
                "politically_exposed",
            ),
        )

    @staticmethod
    def _map_profile(data: dict) -> CustomerProfile:
        dob = data.get("date_of_birth")

        return CustomerProfile(
            customer_id=data["uid"],
            name=data.get("name"),
            mobile=data.get("mobile"),
            email=data.get("email"),
            date_of_birth=dob,
            gender=Gender.from_value(data.get("gender")),
            marital_status=MaritalStatus.from_value(
                data.get("marital_status")
            ),
            is_nri=data.get("is_nri", False),
        )

    @staticmethod
    def _map_kyc(data: dict) -> KYC:
        return KYC(
            verified=data.get("is_kyc_verified", False),
            status=KYCStatus.from_value(
                data.get("kyc_status")
            ),
            kra_name=data.get("kra_name"),
            pan_updated=data.get("pan_updated", False),
            pan_documents_uploaded=data.get(
                "pan_kyc_docs_uploaded",
                False,
            ),
        )

    @staticmethod
    def _map_bank(data: dict) -> Bank:
        limit = data.get("nach_upper_limit_amount")

        return Bank(
            bank_name=data.get("bank_name"),
            verified=data.get("bank_updated", False),
            validated=data.get("bank_validated", False),
            updated=data.get("bank_updated", False),
            mandate_status=data.get(
                "nach_mandate_status"
            ),
            mandate_limit=Decimal(str(limit))
            if limit is not None
            else None,
            auto_debit_enabled=data.get(
                "debit_enabled",
                False,
            ),
        )

    @staticmethod
    def _map_nominee(
        nominee: dict | None,
    ) -> Nominee:

        if not nominee:
            return Nominee()

        return Nominee(
            exists=True,
            name=nominee.get("nominee_name"),
            relationship=nominee.get(
                "nominee_relationship"
            ),
            date_of_birth=CustomerMapper._parse_date(
                nominee.get("nominee_date_of_birth")
            ),
            guardian=nominee.get(
                "nominee_guardian"
            ),
            identity_type=NomineeIdentityType.from_value(
                nominee.get("nominee_id_type")
            ),
            identity_number=nominee.get(
                "nominee_id_no"
            ),
            email=nominee.get(
                "nominee_email_id"
            ),
            mobile=nominee.get(
                "nominee_mobile_no"
            ),
        )

    @staticmethod
    def _map_investment(data: dict) -> Investment:
        return Investment(
            investment_allowed=data.get(
                "ok_for_investment",
                False,
            ),
            has_investments=data.get(
                "has_investments",
                False,
            ),
            risk_profile=data.get(
                "risk_category"
            ),
            last_payment_mode=data.get(
                "last_payment_mode"
            ),
            regular_investment_allowed=data.get(
                "is_able_to_invest_regular",
                False,
            ),
            direct_plan_enabled=data.get(
                "settings",
                {},
            ).get("direct_enabled", False),
            regular_plan_enabled=data.get(
                "settings",
                {},
            ).get("regular_enabled", False),
        )

    @staticmethod
    def _map_onboarding(data: dict) -> Onboarding:
        return Onboarding(
            status=data.get(
                "onboarding_status"
            ),
            error=data.get(
                "onboarding_error"
            ),
        )

    @staticmethod
    def _map_onboarding_details(
        data: dict,
    ) -> OnboardingDetails:

        return OnboardingDetails(
            ok_for_investment=data.get("ok_for_investment", False),
            bank_updated=data.get("bank_updated", False),
            bank_validated=data.get("bank_validated", False),
            fatca_updated=data.get("fatca_updated",False),
            email_verified=data.get("is_email_verified", False),
            mobile_verified=data.get("mobile_verified", False),
            address_updated=data.get("address_updated",False),
            signature_status=SignatureStatus.from_value(data.get("signature_status")),
            onboarding_status=OnboardingStatus.from_value(data.get("onboarding_status")),
            kyc_status=KYCStatus.from_value(data.get("kyc_status")),
        )

    @staticmethod
    def _map_preferences(
        settings: dict | None,
    ) -> CustomerPreferences:
        settings = settings or {}

        return CustomerPreferences(
            push_notifications_enabled=settings.get(
                "push_enabled",
                False,
            ),
            newsletter_enabled=settings.get(
                "newsletter_enabled",
                False,
            ),
            summary_day=settings.get(
                "summary_day"
            ),
            reminder_days=settings.get(
                "remind_days"
            ),
            payment_preference=settings.get(
                "payment_preference"
            ),
        )

    @staticmethod
    def _parse_date(
        value: str | None,
    ) -> date | None:
        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            return None

    @staticmethod
    def _calculate_age(
        dob: date | None,
    ) -> int | None:
        if dob is None:
            return None

        today = date.today()

        return (
            today.year
            - dob.year
            - (
                (today.month, today.day)
                < (dob.month, dob.day)
            )
        )