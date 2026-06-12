from abc import abstractmethod, ABC

from ingestion.models import Chunk, ParsedSchemeDocument

class Chunker(ABC):

    @abstractmethod
    def generate_chunks(self, document: ParsedSchemeDocument) -> list[Chunk]:
        raise NotImplementedError