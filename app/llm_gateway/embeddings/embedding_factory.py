from app.llm_gateway.embeddings.bedrock_embedding_client import BedrockEmbeddingClient

class EmbeddingFactory:

    @staticmethod
    def get_client():
        return BedrockEmbeddingClient()