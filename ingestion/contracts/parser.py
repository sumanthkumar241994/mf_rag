from abc import abstractmethod, ABC
from ingestion.models import ParsedDocument, ParsedSchemeDocument

class Parser(ABC):
    
    @abstractmethod
    def parse(self, document: ParsedDocument) -> ParsedSchemeDocument:
        """
        Converts a raw parsed dodcument to a 
        structured scheme document
        """
        raise NotImplementedError
