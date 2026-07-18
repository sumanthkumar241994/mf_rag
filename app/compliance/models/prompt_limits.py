from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PromptLimits:
    max_prompt_tokens: int
    require_context: bool