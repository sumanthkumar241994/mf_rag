from app.events.publishers.sqs_publisher import SQSEventPublisher
from app.llm_gateway.llm_gateway import LLMGateway
from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider


class LLMComposition:
    def __init__(self):
        self.gemma_provider = GemmaProvider()
        self.sqs_publisher = SQSEventPublisher()
        self.gateway = LLMGateway(provider=self.gemma_provider, sqs_publisher=self.sqs_publisher)
        