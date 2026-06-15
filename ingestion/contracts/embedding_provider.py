from abc import abstractmethod, ABC

class EmbeddingProvider(ABC):

    @abstractmethod
    def generate(self, text: str) -> list[float]:
        """Generate emedding for a given gext"""
        raise NotImplementedError

    @abstractmethod
    def generate_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a batch of texts
        """
        raise NotImplementedError