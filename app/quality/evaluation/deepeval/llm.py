from __future__ import annotations

import asyncio
from typing import Any

from deepeval.models import DeepEvalBaseLLM

from app.dtos.llm.llm_request import LLMRequest
from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.llm_gateway import LLMGateway


class AdvisorJudgeLLM(DeepEvalBaseLLM):
    """
    DeepEval wrapper around our LLMGateway.

    DeepEval should never know anything about Bedrock,
    Claude, retries, authentication, or providers.
    """

    def __init__(
        self,
        gateway: LLMGateway,
    ) -> None:
        self._gateway = gateway

    def load_model(self) -> Any:
        """
        DeepEval requires this method.
        Since we're routing everything through our LLMGateway,
        there's no underlying model object to return.
        """
        return self

    def get_model_name(self) -> str:
        return ModelProfile.JUDGE.value

    async def a_generate(
        self,
        prompt: str,
    ) -> str:
        response = await self._gateway.generate(
            request=LLMRequest(
                system_prompt="",
                user_prompt=prompt,
                temperature=0,
            ),
            model_profile=ModelProfile.JUDGE,
            trace=False
        )

        return response.answer

    def generate(
        self,
        prompt: str,
    ) -> str:
        return asyncio.run(self.a_generate(prompt))