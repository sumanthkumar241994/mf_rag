from app.dtos.llm.llm_request import LLMRequest
from app.models.message import Message


class ConversationTitlePromptBuilder:

    SYSTEM_PROMPT = """
        You generate concise conversation titles.

        Rules:
        - Maximum 6 words.
        - Do not use quotes.
        - Do not use punctuation unless required.
        - Use title case.
        - Capture the primary customer intent.
        - Do not mention "User", "Assistant", or "Conversation".
        - Return only the title.
    """

    def build(self, messages: list[Message]) -> LLMRequest:
        conversation = self._format_messages(messages)
        user_prompt = f"""
            Generate a short title for the following conversation.

            Conversation:

            {conversation}
        
        """.strip()

        return LLMRequest(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.2,
            max_tokens=20,
        )

    @staticmethod
    def _format_messages(messages: list[Message]) -> str:
        lines: list[str] = []
        for message in messages:
            lines.append(f"{message.role.value.title()}: {message.content}")

        return "\n".join(lines)