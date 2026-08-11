from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.data_collection_builder import DataCollectionBuilder
from app.investment.models.data_collection import DataCollection
from app.investment.workflows.investment_state import InvestmentState


class NomineeCollectionBuilder(DataCollectionBuilder):

    def build(
        self,
        state: InvestmentState,
    ) -> DataCollection:

        nominee = state.customer.nominee

        return DataCollection(
            entity="NOMINEE",
            title="Nominee Details",
            message="Please complete the nominee details.",

            existing_data={
                "name": nominee.name,
                "relationship": nominee.relationship,
                "date_of_birth": nominee.date_of_birth,
                "guardian": nominee.guardian,
                "identity_type": (
                    nominee.identity_type.value
                    if nominee.identity_type
                    else None
                ),
                "identity_number": nominee.identity_number,
                "email": nominee.email,
                "mobile": nominee.mobile,
            },

            missing_fields=[
                field.value
                for field in nominee.missing_fields
            ],

            editable=True,
            otp_required=True,
        )