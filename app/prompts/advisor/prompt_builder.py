from app.schemas.conversation.cache_message import CacheMessage
from app.workflows.advisor.advisor_state import AdvisorState

class AdvisorPromptBuilder:
    """
    Builds the user prompt for the Advisor workflow.
    """

    @staticmethod
    def build(state: AdvisorState):
        parts : list[str] = []
        if state['history']:
            parts.append("## Conversation History")

            for message in state['history']:
                parts.append(f"{message.role}: {message.content}")
        
        if state['context']:
            parts.append("")
            parts.append("## Retrieved Context")
            parts.append(state['context'])

        parts.append("")
        parts.append("## Current User Question")
        parts.append(state['query'])

        return "\n".join(parts)