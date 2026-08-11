from abc import ABC, abstractmethod

from app.investment.models.data_collection import DataCollection
from app.investment.workflows.investment_state import InvestmentState


class DataCollectionBuilder(ABC):

    @abstractmethod
    def build(self, state: InvestmentState) -> DataCollection:
        ...