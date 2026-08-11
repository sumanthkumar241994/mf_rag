from app.investment.business.execution.customer.builder.fatca_data_collection_builder import FatcaCollectionBuilder
from app.investment.business.execution.customer.builder.nominee_data_collection_builder import NomineeCollectionBuilder
from app.investment.business.execution.data_collection_builder import DataCollectionBuilder
from app.investment.common.enums.eligibility_requirement_type import EligibilityRequirementType


class CustomerDataCollectionBuilderRegistry:

    def __init__(
        self,
        nominee_builder: NomineeCollectionBuilder,
        fatca_builder: FatcaCollectionBuilder,
    ):
        self._builders = {
            EligibilityRequirementType.NOMINEE: nominee_builder,
            EligibilityRequirementType.FATCA: fatca_builder
        }

    def get(
        self,
        requirement: EligibilityRequirementType,
    ) -> DataCollectionBuilder:
        return self._builders[requirement]