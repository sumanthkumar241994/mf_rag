# app/api/dependencies/llm.py
from app.llm_gateway.embeddings.bedrock_titan_embedding import BedrockTitanEmbedding
from app.llm_gateway.enums.provider import Provider
from app.llm_gateway.llm_gateway import LLMGateway
from app.llm_gateway.providers.bedrock_claude_gateway import AnthropicProvider
from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider
from app.events.publishers.sqs_publisher import SQSEventPublisher

def get_llm_gateway() -> LLMGateway:
    return LLMGateway(
        sqs_publisher=SQSEventPublisher(),
        providers={
            Provider.ANTHROPIC: AnthropicProvider(),
            Provider.GEMMA: GemmaProvider(),
            Provider.TITAN: BedrockTitanEmbedding()
        }
    )