from ingestion.metadata.models.scheme_metadata import SchemeMetaData
from ingestion.models.parsed_document import ParsedDocument
from .resolvers.amc_resolver import AMCResolver
from .extractors.scheme_name_extractor import SchemeNameExtractor
from ingestion.metadata.resolvers import amc_resolver

class MetaDataExtractor:
    PAGE_SCAN_LIMIT = 3

    def __init__(self) -> None:
        self.amc_resolver = AMCResolver()
        self.scheme_name_extractor = SchemeNameExtractor()

    def extract(self, document: ParsedDocument) -> SchemeMetaData:
        text = self._build_metadata_text(document)
        amc_name = self.amc_resolver.resolve(text)
        scheme_name = self.scheme_name_extractor.extract(text)

        return SchemeMetaData(
            scheme_name=scheme_name,
            amc_name=amc_name
        )
    

    def _build_metadata_text(self, document: ParsedDocument) -> str:
        pages = [page for page in document.pages[:self.PAGE_SCAN_LIMIT]]
        return "\n".join(pages)

