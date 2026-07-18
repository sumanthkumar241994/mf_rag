from dataclasses import dataclass


@dataclass(slots=True)
class SanitizedPrompt:
    system_prompt: str
    user_prompt: str