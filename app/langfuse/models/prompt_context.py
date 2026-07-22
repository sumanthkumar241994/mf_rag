from dataclasses import dataclass


@dataclass(slots=True)
class PromptContext:
    system_prompt_length: int
    user_prompt_length: int
    total_prompt_length: int