from app.llm_gateway.providers.bedrock_claude_gateway import AnthropicProvider

class LLMRouter:
    @staticmethod
    def get_provider():
        return AnthropicProvider()