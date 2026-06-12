from ingestion.constants import DocumentType
from ingestion.models import ParsedDocument, ParsedSchemeDocument

from .boundary_builder import SIDSectionBoundaryBuilder
from .heading_extractor import SIDHeadingExtractor
from .metadata_extractor import SIDMetaDataExtractor
from .section_extractor import SIDSectionExtractor
from .toc_extractor import SIDTOCExractor

class SIDParser:

    def __init__(self):
        self.toc_extractor = SIDTOCExractor()
        self.heading_extractor = SIDHeadingExtractor()
        self.boundary_builder = SIDSectionBoundaryBuilder()
        self.section_extractor = SIDSectionExtractor()
        self.metadata_extractor = SIDMetaDataExtractor()

    def parse(self, document: ParsedDocument) -> ParsedSchemeDocument:
        markers = self.toc_extractor.extract(document=document)

        if not markers:
            markers = self.heading_extractor.extract(document=document)
        
        boundaries = self.boundary_builder.build(
            total_pages=document.page_count, 
            markers=markers
            )
        
        sections = self.section_extractor.extract(
            document=document,
            boundaries=boundaries
            )
        
        metadata = self.metadata_extractor.extract(document=document)

        return ParsedSchemeDocument(
            document_type=DocumentType.SID,
            amc_name=metadata.get("amc_name"),
            scheme_name=metadata.get("scheme_name"),
            sections=sections,
            metadata=metadata
        )
