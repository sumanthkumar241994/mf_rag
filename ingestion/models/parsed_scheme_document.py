from dataclasses import dataclass, field
from datetime import date

from .document_section import DocumentSection
from ingestion.constants import DocumentType    


@dataclass(slots=True)
class ParsedSchemeDocument:
    document_type: DocumentType
    amc_name: str
    scheme_name: str
    scheme_code: str | None = None
    effective_date: date | None = None
    sections: list[DocumentSection] = field(default_factory=list)
    metadata: list = field(default_factory=dict)