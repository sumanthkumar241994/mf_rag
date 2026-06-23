from app.llm_gateway.providers.anthropic_client import AnthropicProvider

class LLMRouter:
    @staticmethod
    def get_provider():
        return AnthropicProvider()