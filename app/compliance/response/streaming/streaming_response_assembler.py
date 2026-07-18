from dataclasses import dataclass
import re

from app.compliance.response.policy_executor import PolicyExecutor
from app.compliance.response.streaming.stream_result import StreamResult
from app.compliance.response.streaming.stream_state import StreamState


class StreamingResponseAssembler:
    """
    Buffers streamed text until complete sentences are available,
    then passes each sentence through the policy pipeline.
    """

    def __init__(self, executor: PolicyExecutor):
        self._executor = executor

    async def process_chunk(
        self,
        state: StreamState,
        chunk: str,
    ) -> StreamResult:

        if not chunk:
            return StreamResult(chunk="")

        state.complete_response += chunk
        state.buffer += chunk

        sentences, remainder = self._extract_sentences(state.buffer)

        state.buffer = remainder

        if not sentences:
            return StreamResult(chunk="")

        output: list[str] = []

        for sentence in sentences:
            
            result = await self._executor.execute(
                state.request.with_text(sentence)
            )
            
            state.findings.extend(result.findings)

            if result.blocked:
                state.blocked = True
                state.reason = result.reason

                return StreamResult(
                    chunk="",
                    blocked=True,
                    reason=result.reason,
                )

            output.append(result.request.text)

        processed_chunk = "".join(output)
        state.processed_response += processed_chunk

        return StreamResult(
            chunk=processed_chunk
        )

    async def finalize(
    self,
    state: StreamState,
    ) -> StreamResult:

        if not state.buffer:
            return StreamResult(
                processed_response=state.processed_response,
                completed=True,
            )

        result = await self._executor.execute(
            state.request.with_text(state.buffer)
        )

        state.findings.extend(result.findings)
        state.buffer = ""

        if result.blocked:
            state.blocked = True
            state.reason = result.reason

            return StreamResult(
                blocked=True,
                completed=True,
                reason=result.reason,
                processed_response=state.processed_response,
            )

        # Append the last processed chunk
        state.processed_response += result.request.text

        return StreamResult(
            chunk=result.request.text,
            processed_response=state.processed_response,
            completed=True,
        )

    @staticmethod
    def _extract_sentences(
        text: str,
    ) -> tuple[list[str], str]:

        sentences: list[str] = []

        start = 0

        for i, ch in enumerate(text):
            if ch in ".!?\n":
                sentences.append(text[start:i + 1])
                start = i + 1

        return (
            sentences,
            text[start:],
        )