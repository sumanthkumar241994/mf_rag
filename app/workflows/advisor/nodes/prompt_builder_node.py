from typing import AsyncIterator
from app.dtos.agents.stream_event import AgentStreamEvent
from app.enums.stream_event_type import StreamEventType
from app.prompts.advisor.prompt_builder import AdvisorPromptBuilder
from app.workflows.advisor.advisor_state import AdvisorState


class PromptBuilderNode:
    def __init__(self, prompt_builder: AdvisorPromptBuilder):
        self._prompt_builder = prompt_builder
    
    def __call__(self, state: AdvisorState) -> AdvisorState:
        state.prompt = self._prompt_builder.build(state)

        return state

    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:
        yield AgentStreamEvent(
            type=StreamEventType.PROMPT_START.value
        )

        state.prompt = self._prompt_builder.build(state)

        yield AgentStreamEvent(
            type=StreamEventType.PROMPT_END.value,
            metadata={
                "prompt_length": len(state.prompt.user_prompt)
            }
        )