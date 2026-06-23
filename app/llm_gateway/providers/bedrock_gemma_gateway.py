import json
import asyncio

from app.core.config.settings import settings
from app.core.config.aws import AWS

from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse

from app.llm_gateway.providers.base import LLMProvider

class GemmaProvider(LLMProvider):
    MODEL_ID = settings.BEDROCK_GEMMA_MODEL_ID

    def __init__(self):
        self.bedrock_client = AWS().bedrock_runtime

    async def generate(self, request: LLMRequest) -> LLMResponse:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system": request.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Question: 
                    {request.query}

                    Context:
                    {request.context}
                    """
                }
            ]
        }

        response = await asyncio.to_thread(self.bedrock_client.invoke_model,modelId=self.MODEL_ID, body=json.dumps(body))
        response_body = json.loads(response['body'].read())
        answer = response_body['choices'][0]['message']['content']

        return LLMResponse(answer=answer, model=self.MODEL_ID)