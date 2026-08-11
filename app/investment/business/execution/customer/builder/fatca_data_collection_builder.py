from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.data_collection_builder import DataCollectionBuilder
from app.investment.models.data_collection import DataCollection
from app.investment.workflows.investment_state import InvestmentState


class FatcaCollectionBuilder(DataCollectionBuilder):

    def build(
        self,
        state: InvestmentState,
    ) -> DataCollection:

        fatca = state.customer.fatca

        return DataCollection(
            entity="FATCA",
            title="FATCA Details",
            message="Please complete the missing FATCA details.",
            existing_data={
                "occupation_code": (
                    fatca.occupation_code.value
                    if fatca.occupation_code
                    else None
                ),
                "annual_income_code": (
                    fatca.annual_income_code.value
                    if fatca.annual_income_code
                    else None
                ),
                "source_of_wealth_code": (
                    fatca.source_of_wealth_code.value
                    if fatca.source_of_wealth_code
                    else None
                ),
                "birth_country": fatca.birth_country,
                "address_type": (
                    fatca.address_type.value
                    if fatca.address_type
                    else None
                ),
                "is_indian_tax_payer": fatca.is_indian_tax_payer,
                "politically_exposed": fatca.politically_exposed,
            },
            missing_fields=[
                field.value
                for field in fatca.missing_fields
            ],
        )