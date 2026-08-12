from typing import Any
from app.investment.base.models import InvestmentBaseModel


class DataCollection(InvestmentBaseModel):
    entity: str
    action: str
    title: str

    message: str

    existing_data: dict[str, Any]

    missing_fields: list[str]