from abc import ABC, abstractmethod

class EmbeddingClient(ABC):
    @abstractmethod
    async def generate(self, text: str) -> list[float]:
        raise NotImplementedError