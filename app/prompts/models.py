from dataclasses import dataclass

from app.prompts.enums import PromptType


@dataclass(slots=True)
class Prompt:
    type: PromptType
    version: str

    system_prompt: str
    user_prompt: str

    @property
    def name(self) -> str:
        return f"{self.type}:{self.version}"