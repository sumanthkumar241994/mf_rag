
from app.llm_gateway.embeddings.bedrock_titan_embedding import BedrockTitanEmbedding


class EmbeddingFactory:

    @staticmethod
    def get_client():
        return BedrockTitanEmbedding()