from dataclasses import dataclass
from app.schemas.responses.retrieval import RetrievedChunk

@dataclass(slots=True)
class LLMContext:
    """
    Context object passed to LLM layer

    Attributes:
        context:
            formatted context string sent to the LLM
        
        source_map:
            Maps source_id to Retrieved chunk

        chunk_count:
            Number of chunks included in final context
        
        total_characters:
            Total size of generated context
        
        truncated:
            True if some retrieved chunks were excluded due to context size limit
        
    """
    context: str
    source_map: dict[int,RetrievedChunk]
    chunk_count: int
    total_characters: int
    truncated: bool