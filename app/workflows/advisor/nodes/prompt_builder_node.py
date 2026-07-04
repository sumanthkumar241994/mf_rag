from app.prompts.advisor.prompt_builder import AdvisorPromptBuilder
from app.workflows.advisor.advisor_state import AdvisorState


class PromptBuilderNode:
    def __init__(self, prompt_builder: AdvisorPromptBuilder):
        self._prompt_builder = prompt_builder
    
    def __call__(self, state: AdvisorState) -> AdvisorState:
        state.prompt = self._prompt_builder.build(state)

        return state