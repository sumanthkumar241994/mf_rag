import asyncio

from app.dtos.llm.llm_request import LLMRequest

from app.llm_gateway.llm_gateway import LLMGateway
from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider


async def main():

    gateway = LLMGateway(
        GemmaProvider()
    )

    request = LLMRequest(
        system_prompt="You are a helpful assistant.",
        user_prompt="What are mutual fund risk factors?",
        max_tokens=500,
        temperature=0.0,
    )

    async for token in gateway.stream(
        request
    ):
        print(token, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())