from ingestion.chunking.config import ChunkingConfig
from ingestion.chunking.models.chunk import Chunk
from ingestion.chunking.models.chunk_metadata import ChunkMetadata

from ingestion.chunking.section_category_resolver import SectionCategoryResolver
from ingestion.chunking.subheading_detector import SubHeadingDetector
from ingestion.chunking.token_window_chunker import TokenWindowChunker
from ingestion.models.parsed_scheme_document import ParsedSchemeDocument

class SemanticChunker:
    def __init__(self, config: ChunkingConfig | None = None) -> None:
        self.config = config or ChunkingConfig
        self.subheading_detector = SubHeadingDetector()
        self.category_resolver = SectionCategoryResolver()
        self.window_chunker = TokenWindowChunker(self.config)
    
    def chunk(self, scheme_doc: ParsedSchemeDocument) -> list[Chunk]:
        chunks = []
        chunk_order = 1

        for section in scheme_doc.sections:
            section_category = self.category_resolver.resolve(section.title)

            if section_category == 'others':
                continue

            segments = self.subheading_detector.detect(content=section.content,page_number=section.page_number)
            if not segments:
                segments = [{
                    "title": section.title,
                    "content": section.content
                }]

            for segment in segments:
                enriched_text = self._build_chunk_test(section_title=section.title, segment_title=segment.title, content=segment.content)
                split_chunks = self.window_chunker.split(enriched_text)

                for chunk_text in split_chunks:
                    token_count = len(chunk_text.split())

                    if token_count < self.config.min_chunk_tokens:
                        continue
                    
                    chunks.append(
                        Chunk(
                            content=chunk_text,
                            token_count=token_count,
                            metadata=ChunkMetadata(
                                section_title=section.title,
                                page_number=section.page_number,
                                chunk_order=chunk_order,
                                section_category=section_category
                            )
                        )
                    )
        return chunks                  

    
    def _build_chunk_test(self, section_title: str, segment_title: str, content: str) -> str:
        return f"""
        Section: {section_title}

        Subsection: {segment_title}

        {content}
        """.strip()
