from abc import ABC, abstractmethod


class SchemeGateway(ABC):
    @abstractmethod
    async def search(self, query: str, page: int = 1) -> list[dict]:
        pass

    @abstractmethod
    async def get_scheme_details(self, scheme_id: int) -> dict:
        pass