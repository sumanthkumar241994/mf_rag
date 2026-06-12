from dataclasses import dataclass, field
from .toc_entry import TOCEntry
from .section_boundary import SectionBoundary

@dataclass(slots=True)
class DocumentStructure:
    toc_entries: list[TOCEntry] = field(default_factory=list) 
    section_boundaries: list[SectionBoundary] = field(default_factory=list)
