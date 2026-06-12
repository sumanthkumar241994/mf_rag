from abc import abstractmethod, ABC

class EmbeddigProvider(ABC):

    @abstractmethod
    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a batch of texts
        """
        raise NotImplementedError