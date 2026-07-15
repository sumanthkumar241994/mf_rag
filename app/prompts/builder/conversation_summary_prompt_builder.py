from app.dtos.llm.llm_request import LLMRequest
from app.models.message import Message


class ConversationSummaryPromptBuilder:

    SYSTEM_PROMPT = """
        You maintain an incremental conversation summary.

        You will receive:
        1. The previous summary.
        2. New conversation messages.

        Update the summary.

        Rules:
        - Preserve all confirmed facts.
        - Update existing facts if newer information supersedes them.
        - Remove duplicate information.
        - Ignore greetings, acknowledgements and small talk.
        - Ignore workflow/system messages.
        - Keep the summary concise.
        - Always return the following markdown structure exactly.

        # Customer Goal

        # Customer Information

        # Investment Preferences

        # Advice Given

        # Decisions Made

        # Pending Questions

        # Next Follow-up

        If a section has no information, write "None".
        Return only the markdown summary.
    """

    def build(self, previous_summary: str | None, messages: list[Message]) -> LLMRequest:
        previous_summary = previous_summary or "No previous summary."
        conversation = self._format_messages(messages)
        user_prompt = f"""
        Previous Summary
        ----------------
        {previous_summary}

        New Messages
        ------------
        {conversation}

        Update the summary.
        """.strip()

        return LLMRequest(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0,
            max_tokens=1024,
        )

    @staticmethod
    def _format_messages(
        messages: list[Message],
    ) -> str:

        lines: list[str] = []

        for message in messages:
            role = message.role.value.title()
            lines.append(f"{role}: {message.content}")

        return "\n".join(lines)