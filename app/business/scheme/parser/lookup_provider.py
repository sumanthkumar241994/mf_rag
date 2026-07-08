from abc import ABC, abstractmethod

from app.business.scheme.enums.lookup_type import LookupType


class LookupProvider(ABC):

    # @abstractmethod
    # def get_categories(self) -> dict[str, str]:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_scheme_types(self) -> dict[str, str]:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_amcs(self) -> dict[str, str]:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_investment_options(self) -> dict[str, str]:
    #     raise NotImplementedError

    @abstractmethod
    def lookup(self, lookup_type: LookupType) -> dict[str, str] | list[str]:
        raise NotImplementedError