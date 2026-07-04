from dataclasses import dataclass


@dataclass(slots=True)
class Prompt:
    system_prompt: str
    user_prompt: str
    final_prompt: str | None = None