from app.compliance.response.models.response_compliance_request import (
    ResponseComplianceRequest,
)
from app.compliance.response.streaming.stream_state import StreamState
from app.compliance.response.streaming.streaming_response_assembler import StreamingResponseAssembler
from tests.models.streaming_test_result import StreamingTestResult


class StreamingTestHarness:
    """
    Test helper that simulates an LLM streaming response.

    Example:

        harness = StreamingTestHarness(assembler)

        result = await harness.execute(
            text="Contact me at abc@gmail.com",
            chunk_size=5,
        )

        assert result == "Contact me at [EMAIL REDACTED]"
    """

    def __init__(
        self,
        assembler: StreamingResponseAssembler,
    ) -> None:
        self._assembler = assembler

    async def execute(
        self,
        text: str,
        chunk_size: int = 10,
        request: ResponseComplianceRequest | None = None,
    ) -> StreamingTestResult:

        if request is None:
            request = ResponseComplianceRequest(
                response="",
            )

        state = StreamState(
            request=request,
        )

        output: list[str] = []

        for chunk in self._chunk(text, chunk_size):
            
            result = await self._assembler.process_chunk(
                chunk=chunk,
                state=state,
            )

            output.append(result.chunk)

            if result.blocked:
                break

        result = await self._assembler.finalize(state)

        output.append(result.chunk)

        return StreamingTestResult(
            output="".join(output),
            state=state,
        )

    @staticmethod
    def _chunk(
        text: str,
        chunk_size: int,
    ):

        for index in range(0, len(text), chunk_size):
            yield text[index:index + chunk_size]