# app/api/dependencies/llm.py
from app.llm_gateway.llm_gateway import LLMGateway
from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider
from app.events.publishers.sqs_publisher import SQSEventPublisher

def get_llm_gateway() -> LLMGateway:
    return LLMGateway(provider=GemmaProvider(), sqs_publisher=SQSEventPublisher())