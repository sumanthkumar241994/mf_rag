import time
import json
import asyncio

from app.core.config.settings import settings
from app.core.config.aws import AWS

from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics
from app.dtos.llm.llm_stream_response import LLMStreamResponse

from app.llm_gateway.providers.base import LLMProvider

from app.observability.tracing import trace_step
import logging

logger = logging.getLogger(__name__)

class GemmaProvider(LLMProvider):
    MODEL_ID = settings.BEDROCK_GEMMA_MODEL_ID

    def __init__(self):
        self.bedrock_client = AWS().bedrock_runtime

    @trace_step("llm_runtime_generate")
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
                    {request.user_prompt}

                    Context:
                    {request.context}
                    """
                }
            ]
        }
        start_time = time.perf_counter()
        
        response = await asyncio.to_thread(self.bedrock_client.invoke_model,modelId=self.MODEL_ID, body=json.dumps(body))

        latency_ms = round((time.perf_counter() - start_time)*1000)

        response_body = json.loads(response['body'].read())
        logger.info(f"Gemma API Response: {response_body}")
        choice = response_body['choices'][0]
        answer = choice['message']['content']
        usage = response_body['usage']

        return LLMResponse(
            answer=answer, 
            usage=LLMUsage(
                input_tokens=usage['prompt_tokens'],
                output_tokens=usage['completion_tokens'],
                total_tokens= usage['total_tokens']
            ),
            metrics = LLMMetrics(
                model=self.MODEL_ID,
                latency_ms=latency_ms,
                finish_reason=choice.get('finish_reason')
            )
        )

    @trace_step("llm_runtime_stream")
    async def stream(self, request: LLMRequest, stream_response: LLMStreamResponse):
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
                    {request.user_prompt}

                    Context:
                    {request.context}
                    """
                }
            ]
        }

        response = await asyncio.to_thread(
            self.bedrock_client.invoke_model_with_response_stream,
            modelId=self.MODEL_ID,
            body=json.dumps(body)
        )

        stream = response['body']

        for event in stream:
            chunk = event.get('chunk')
            if not chunk:
                continue

            payload = json.loads(chunk['bytes'].decode('utf-8'))

            choices = payload.get('choices', [])
            if not choices:
                continue

            delta = choices[0].get("delta",{})
            if not delta:
                continue

            content = delta.get("content")

            if "<reasoning>" not in content and "</reasoning>" not in content :
                stream_response.answer += content
                yield content

            # Final Chunk
            invocation_metrics = payload.get("amazon-bedrock-invocationMetrics")

            if invocation_metrics:
                stream_response.usage = LLMUsage(
                    input_tokens=invocation_metrics['inputTokenCount'],
                    output_tokens=invocation_metrics['outputTokenCount'],
                    total_tokens =invocation_metrics['inputTokenCount'] + invocation_metrics['outputTokenCount']
                )

                stream_response.metrics = LLMMetrics(
                    model = self.MODEL_ID,
                    latency_ms=invocation_metrics['invocationLatency'],
                    first_token_latency_ms=invocation_metrics['firstByteLatency'],
                    invocation_latency_ms=invocation_metrics['invocationLatency'],
                    finish_reason=choices[0].get('finish_reason')
                )


