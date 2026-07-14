from collections import OrderedDict

from app.business.document.models.llm_context import LLMContext
from app.business.document.models.retrieved_chunk import RetrievedChunk

class ContextBuilder:
    """
    Build LLM Ready context from retrieved chunks

    Responsibilities:
    - Deduplicate chunks
    - Normalize metadata
    - Build source references
    - Enforce token/character budget
    - Produce deterministic cotext ordering
    """

    def __init__(self, max_context_chars: int = 50000):
        self.max_context_chars = max_context_chars

    def build(self, chunks: list[RetrievedChunk]) -> LLMContext:
        """
        Returns:
            context: formatted context string
            source_map: source_id -> chunk mapping
        """

        if not chunks:
            return "", {}

        unique_chunks = self._deduplicate(chunks)
        context_parts : list[str] = []
        source_map: dict[int, RetrievedChunk] = {}

        current_size = 0

        for source_id,chunk in enumerate(unique_chunks, start=1):
            block = self._build_chunk_block(
                source_id=source_id,
                chunk=chunk
            )

            block_size = len(block)
        
            if current_size + block_size > self.max_context_chars:
                break

            context_parts.append(block)

            source_map[source_id] = chunk
            current_size += block_size

        context = "\n\n".join(context_parts)

        return LLMContext(
            context=context,
            source_map=source_map,
            chunk_count=len(source_map),
            total_characters=current_size,
            truncated=len(unique_chunks) > len(source_map)
        )


    @staticmethod
    def _deduplicate(chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        unique = OrderedDict()
        for chunk in chunks:
            key = chunk.chunk_id

            if key not in unique:
                unique[key] = chunk
            
        return list(unique.values())

    @staticmethod
    def _build_chunk_block(source_id: int, chunk: RetrievedChunk) -> str:
        scheme_name = chunk.scheme_name or "unknown"
        amc_name = chunk.amc_name or "unknown"
        document_type = chunk.document_type or "unknown"
        section_name = chunk.section_name or "unknown"
        page_no = chunk.page_no or "unknown"

        return f"""
        [soruce {source_id}]

        Fund: {scheme_name}
        AMC: {amc_name}
        Document_type: {document_type}
        Section: {section_name}
        Page: {page_no}

        Content: {chunk.content}
        """.strip()

