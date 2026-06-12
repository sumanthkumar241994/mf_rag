from abc import abstractmethod, ABC
from ingestion.models import ParsedDocument

class Loader(ABC):

    @abstractmethod
    def load(self, file_path: str) -> ParsedDocument:
        """
        Reads a document a return the page-wise extracted text
        """
        raise NotImplementedError

