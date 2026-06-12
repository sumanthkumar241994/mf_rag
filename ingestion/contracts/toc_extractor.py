from abc import abstractmethod, ABC
from ingestion.models import ParsedDocument, SectionMarker

class TOCExtractor(ABC):
    
    @abstractmethod
    def extract(self, document: ParsedDocument) -> list[SectionMarker]:
        raise NotImplementedError