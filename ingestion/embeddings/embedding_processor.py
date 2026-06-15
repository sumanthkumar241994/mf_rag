from app.core.config.aws import AWS

from ingestion.chunking import ChunkHasher, ChunkNormalizer
from ingestion.chunking.models import Chunk
from app.repositories.document_chunk import DocumentChunkRepository
from ingestion.providers.bedrock.titan_embedding_generator import BedrockEmebddingGenerator

class EmbeddingProcessor:

    def __init__(
        self,
        db
        ):
        self.chunk_normalizer = ChunkNormalizer()
        self.chunk_hasher = ChunkHasher()
        self.chunk_repository = DocumentChunkRepository(db)
        self.embedding_generator = BedrockEmebddingGenerator(AWS().bedrock_runtime)

    def process(self, chunk: Chunk):
        normalized_content = self.chunk_normalizer.normalize(chunk.content)
        chunk_hash = self.chunk_hasher.generate(normalized_content)
        existing_chunk = self.chunk_repository.find_by_hash(chunk_hash)

        if existing_chunk:
            return existing_chunk

        embedding = self.embedding_generator.generate(normalized_content)

        return self.chunk_repository.create(
            chunk_hash=chunk_hash,
            content=normalized_content,
            token_count=chunk.token_count,
            embedding_model=self.embedding_generator.MODEL_ID,
            embedding=embedding
            )