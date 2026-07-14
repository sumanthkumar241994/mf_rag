from app.prompts.builder.advisor.advisor_prompt_builder import AdvisorPromptBuilder
from app.workflows.advisor.advisor_state import AdvisorState
from langgraph.config import get_stream_writer

class PromptBuilderNode:
    """
    Builds the final prompt that will be sent to the LLM.
    """

    def __init__(
        self,
        prompt_builder: AdvisorPromptBuilder,
    ):
        self._prompt_builder = prompt_builder

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:
        writer = get_stream_writer()

        writer(
            {
                "type": "prompt_start",
            }
        )
        state.prompt = self._prompt_builder.build(state)

        return state