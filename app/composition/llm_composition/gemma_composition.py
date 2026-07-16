from app.events.publishers.sqs_publisher import SQSEventPublisher
from app.llm_gateway.embeddings.bedrock_titan_embedding import BedrockTitanEmbedding
from app.llm_gateway.enums.provider import Provider
from app.llm_gateway.llm_gateway import LLMGateway
from app.llm_gateway.providers.bedrock_claude_gateway import AnthropicProvider
from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider


class LLMComposition:
    def __init__(self):
        self.providers={
            Provider.ANTHROPIC: AnthropicProvider(),
            Provider.GEMMA: GemmaProvider(),
            Provider.TITAN: BedrockTitanEmbedding()
        }
        self.sqs_publisher = SQSEventPublisher()
        self.gateway = LLMGateway(providers=self.providers, sqs_publisher=self.sqs_publisher)
        