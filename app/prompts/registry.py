from app.prompts.enums import PromptType
from app.prompts.evaluator.builder.base_prompt_builder import BasePromptBuilder


class PromptRegistry:

    def __init__(self) -> None:
        self._builders: dict[PromptType, BasePromptBuilder] = {}

    def register(self, builder: BasePromptBuilder) -> None:
        if builder.type in self._builders:
            raise ValueError(
                f"Prompt builder already registered for '{builder.type}'."
            )

        self._builders[builder.type] = builder

    def get(
        self,
        prompt_type: PromptType,
    ) -> BasePromptBuilder:
        try:
            return self._builders[prompt_type]
        except KeyError as exc:
            raise ValueError(
                f"No prompt builder registered for '{prompt_type}'."
            ) from exc