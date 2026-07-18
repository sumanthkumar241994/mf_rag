from dataclasses import dataclass

from app.dtos.llm.llm_request import LLMRequest



@dataclass(slots=True)
class PromptComplianceRequest:
    prompt: LLMRequest