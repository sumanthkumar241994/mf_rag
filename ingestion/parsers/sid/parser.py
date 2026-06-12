from ingestion.constants import DocumentType
from ingestion.models import ParsedDocument, ParsedSchemeDocument

from .boundary_builder import SectionBoundaryBuilder
from .heading_extractor import SIDHeadingExtractor
from .heading_verifier import SIDHeadingVerifier
from .metadata_extractor import SIDMetaDataExtractor
from .section_extractor import SIDSectionExtractor
from .toc_extractor import SIDTOCExtractor

class SIDParser:

    def __init__(self):
        self.toc_extractor = SIDTOCExtractor()
        self.heading_extractor = SIDHeadingExtractor()
        self.heading_verifier = SIDHeadingVerifier()
        self.boundary_builder = SectionBoundaryBuilder()
        self.section_extractor = SIDSectionExtractor()
        self.metadata_extractor = SIDMetaDataExtractor()

    def parse(self, document: ParsedDocument) -> ParsedSchemeDocument:
        toc_result = self.toc_extractor.extract(document)
        
        if toc_result.found:
            # extract headings
            markers = self.heading_extractor.extract(
                    document=document,
                    skip_until_page=toc_result.toc_end_page
                    )

            # Verify Headings
            markers = self.heading_verifier.verify(
                toc_titles=toc_result.titles,
                markers=markers,
                )
        else:
            markers = self.heading_extractor.extract(document=document)
        # Build Section Boundaries
        boundaries = self.boundary_builder.build(markers=markers, document=document)
        # Extract Sections
        sections = self.section_extractor.extract(document=document, boundaries=boundaries)
        # Extract Metadata
        metadata = self.metadata_extractor.extract(document)
        # Build Parsed Scheme Document
        return ParsedSchemeDocument(
            document_type=DocumentType.SID,
            amc_name=metadata.get("amc_name"),
            scheme_name=metadata.get("scheme_name"),
            sections=sections,
            metadata=metadata
        )