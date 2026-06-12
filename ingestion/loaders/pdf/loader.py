from pathlib import Path
from ingestion.contracts import Loader
from .extractor import PDFTextExtractor
from .validator import PDFValidator
from ingestion.models import ParsedDocument, Page


class PDFLoader(Loader):

    def __init__(self):
        self.extractor = PDFTextExtractor()
        self.validator = PDFValidator()

    def load(self, file_path: str) -> ParsedDocument:
        pages: list[Page] = self.extractor.extract(file_path=file_path)
        self.validator.validate(pages)

        full_text = "\n".join(page.content for page in pages)

        return ParsedDocument(
            file_name=Path(file_path).name,
            source_path=file_path,
            page_count=len(pages),
            pages=pages,
            full_text=full_text,
            metadata={}
        )

