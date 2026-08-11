import json
import asyncio
import time
from typing import AsyncIterator

from app.core.config.settings import settings
from app.core.config.aws import AWS

from app.dtos.llm.llm_chunk import LLMChunk
from app.dtos.llm.llm_metrics import LLMMetrics
from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse

from app.dtos.llm.llm_usage import LLMUsage
from app.llm_gateway.providers.base import LLMProvider
from app.observability.tracing import trace_step

import logging

logger = logging.getLogger(__name__)

class AnthropicProvider(LLMProvider):

    def __init__(self):
        self.bedrock_client = AWS().bedrock_runtime

    async def generate(self, request: LLMRequest, model_id: str) -> LLMResponse:
        body = self._build_request_body(request)

        start_time = time.perf_counter()
        response = await asyncio.to_thread(self.bedrock_client.invoke_model, modelId=model_id, body=json.dumps(body))

        latency_ms = round((time.perf_counter() - start_time)*1000)

        response_body = json.loads(response["body"].read())
        logger.info("Anthropic API Response: %s", response_body)

        content = response_body.get("content", [])

        answer = "".join(block.get("text", "") for block in content if block.get("type") == "text")

        usage = response_body.get("usage", {})

        return LLMResponse(
            answer=answer,
            usage=LLMUsage(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                total_tokens=(usage.get("input_tokens", 0) + usage.get("output_tokens", 0)),
            ),
            metrics=LLMMetrics(
                model=model_id,
                latency_ms=latency_ms,
                finish_reason=response_body.get("stop_reason"),
            ),
        )


    async def astream(self, request: LLMRequest, model_id: str) -> AsyncIterator[LLMChunk]:
        body = self._build_request_body(request)

        request_start = time.perf_counter()
        first_token_at: float | None = None

        response = await asyncio.to_thread(
            self.bedrock_client.invoke_model_with_response_stream,
            modelId=model_id,
            body=json.dumps(body)
        )

        stream = response['body']

        answer: list[str] = []

        input_tokens = 0
        output_tokens = 0
        stop_reason: str | None = None

        usage: LLMUsage | None = None
        metrics: LLMMetrics | None = None

        for event in stream:
            chunk = event.get('chunk')
            if not chunk:
                continue

            payload = json.loads(chunk['bytes'].decode('utf-8'))

            event_type = payload.get("type")

            match event_type:

                # Message Started
                case "message_start":
                    usage = payload["message"].get("usage", {})

                    input_tokens = usage.get("input_tokens", 0)

                # Ignore
                case "content_block_start":
                    pass

                # Stream Tokens
                case "content_block_delta":

                    delta = payload.get("delta", {})

                    match delta.get("type"):
                        case "text_delta":
                            text = delta.get("text", "")

                            if not text:
                                continue

                            if first_token_at is None:
                                first_token_at = time.perf_counter()

                            answer.append(text)

                            yield LLMChunk(token=text)

                        case "thinking_delta":
                            continue

                        case "signature_delta":
                            continue

                        case "input_json_delta":
                            continue

                        case _:
                            continue

                # Ignore
                case "content_block_stop":
                    pass

                # Usage
                case "message_delta":

                    usage = payload.get("usage", {})
                    output_tokens = usage.get("output_tokens", 0)

                    delta = payload.get("delta", {})
                    stop_reason = delta.get("stop_reason")

                # Completed
                case "message_stop":

                    request_end = time.perf_counter()

                    invocation_latency_ms = int(
                        (request_end - request_start) * 1000
                    )

                    first_token_latency_ms = (
                        int((first_token_at - request_start) * 1000)
                        if first_token_at
                        else None
                    )

                    usage = LLMUsage(
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        total_tokens=input_tokens + output_tokens,
                    )

                    metrics = LLMMetrics(
                        model=model_id,
                        latency_ms=invocation_latency_ms,
                        invocation_latency_ms=invocation_latency_ms,
                        first_token_latency_ms=first_token_latency_ms,
                        finish_reason=stop_reason,
                    )

                    yield LLMChunk(
                        response=LLMResponse(
                            answer="".join(answer),
                            usage=usage,
                            metrics=metrics,
                        )
                    )

                # Future Anthropic Events
                # (thinking, tool_use, citations, etc.)
                case _:
                    continue

    def _build_request_body(self, request: LLMRequest) -> dict:
        return {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system": request.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": request.user_prompt,
                        }
                    ],
                }
            ],
        }
