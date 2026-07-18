import random
import re

import pytest

from app.compliance.enums.compliance_action import ComplianceAction
from app.compliance.enums.severity import Severity
from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.models.prohibited_phrases import (
    ProhibitedPhrase,
    ProhibitedPhrases,
)
from app.compliance.repository.policy_repository import PolicyRepository
from app.compliance.response.policy_executor import PolicyExecutor
from app.compliance.response.streaming.processing_request import (
    ProcessingRequest,
)
from app.compliance.response.streaming.stream_state import StreamState
from app.compliance.response.streaming.streaming_response_assembler import (
    StreamingResponseAssembler,
)
from app.compliance.response.validators.policy_validator import (
    PolicyValidator,
)


# -------------------------------------------------------------------------
# Fake Policy Loader
# -------------------------------------------------------------------------


class FakePolicies:

    def __init__(self):

        self.prompt = None
        self.regulatory_links = None

        self.prohibited_phrases = ProhibitedPhrases(
            blocked=[
                ProhibitedPhrase(
                    pattern=re.compile(
                        r"\bguaranteed\s+return(s)?\b",
                        re.IGNORECASE,
                    ),
                    description="Guaranteed return claim",
                    severity=Severity.HIGH,
                    action=ComplianceAction.REPLACE,
                    replacement="expected returns",
                ),
                ProhibitedPhrase(
                    pattern=re.compile(
                        r"\bassured\s+return(s)?\b",
                        re.IGNORECASE,
                    ),
                    description="Assured return claim",
                    severity=Severity.HIGH,
                    action=ComplianceAction.REPLACE,
                    replacement="potential return",
                ),
                ProhibitedPhrase(
                    pattern=re.compile(
                        r"\brisk[-\s]?free\s+investment(s)?\b",
                        re.IGNORECASE,
                    ),
                    description="Risk free investment claim",
                    severity=Severity.HIGH,
                    action=ComplianceAction.REPLACE,
                    replacement="lower-risk investment",
                ),
                ProhibitedPhrase(
                    pattern=re.compile(
                        r"\bSEBI\s+approved\s+investment(s)?\b",
                        re.IGNORECASE,
                    ),
                    description="Unauthorized SEBI approval",
                    severity=Severity.CRITICAL,
                    action=ComplianceAction.REJECT,
                ),
            ]
        )


class FakePolicyLoader(PolicyLoader):

    def load(self):
        return FakePolicies()


# -------------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------------


@pytest.fixture
def repository():

    return PolicyRepository(
        loader=PolicyLoader(),
    )


@pytest.fixture
def validator(repository):

    return PolicyValidator(repository)


@pytest.fixture
def executor(validator):

    return PolicyExecutor(
        validators=[validator],
    )


@pytest.fixture
def assembler(executor):

    return StreamingResponseAssembler(executor)


# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------


async def stream_text(
    assembler,
    text: str,
    chunk_size: int,
):

    state = StreamState(
        request=ProcessingRequest(text="")
    )

    output = ""

    for i in range(0, len(text), chunk_size):

        chunk = text[i : i + chunk_size]

        result = await assembler.process_chunk(
            state,
            chunk
        )

        output += result.chunk

        if result.blocked:
            break

    final = await assembler.finalize(state)

    output += final.chunk

    return output, state, final


async def stream_chunks(
    assembler,
    chunks,
):

    state = StreamState(
        request=ProcessingRequest(text="")
    )

    output = ""

    for chunk in chunks:

        result = await assembler.process_chunk(
            state,
            chunk,
            
        )

        output += result.chunk

        if result.blocked:
            break

    final = await assembler.finalize(state)

    output += final.chunk

    return output, state, final


# -------------------------------------------------------------------------
# Test 1
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_plain_text(assembler):

    text = "Hello, how can I help you today?"

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=10,
    )

    assert output == text
    assert state.complete_response == text
    assert state.buffer == ""
    assert not state.blocked


# -------------------------------------------------------------------------
# Test 2
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_single_replacement(assembler):

    text = "This fund offers guaranteed returns."

    expected = "This fund offers expected returns."

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=100,
    )
    assert output == expected


# -------------------------------------------------------------------------
# Test 3
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_multiple_replacements(assembler):

    text = (
        "Guaranteed returns. "
        "Assured returns. "
        "Risk free investment."
    )

    expected = (
        "expected returns. "
        "potential return. "
        "lower-risk investment."
    )

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=500,
    )

    assert output == expected
    assert len(state.findings) == 3


# -------------------------------------------------------------------------
# Test 4
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_phrase_split_between_chunks(assembler):

    chunks = [
        "This fund provides guaranteed",
        " returns over five years.",
    ]

    expected = (
        "This fund provides expected returns "
        "over five years."
    )

    output, _, _ = await stream_chunks(
        assembler,
        chunks,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 5
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_phrase_split_inside_word(assembler):

    chunks = [
        "This fund provides guaran",
        "teed returns.",
    ]

    expected = (
        "This fund provides expected returns."
    )

    output, _, _ = await stream_chunks(
        assembler,
        chunks,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 6
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_chunk_size_one(assembler):

    text = "Guaranteed returns"

    expected = "expected returns"

    output, _, _ = await stream_text(
        assembler,
        text,
        chunk_size=1,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 7
# -------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "size",
    [2, 5, 10, 20],
)
async def test_small_chunk_sizes(
    assembler,
    size,
):

    text = "Guaranteed returns"

    expected = "expected returns"

    output, _, _ = await stream_text(
        assembler,
        text,
        chunk_size=size,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 8
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_large_chunk(assembler):

    text = (
        "Lorem ipsum dolor sit amet. "
        "Guaranteed returns are impossible. "
        "Risk free investment should never be promised. "
        "Assured returns are misleading."
    )

    expected = (
        "Lorem ipsum dolor sit amet. "
        "expected returns are impossible. "
        "lower-risk investment should never be promised. "
        "potential return are misleading."
    )

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=200,
    )

    assert output == expected
    assert len(state.findings) == 3


    # -------------------------------------------------------------------------
# Test 9
# Phrase at beginning
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_phrase_at_beginning(assembler):

    text = "Guaranteed returns are not possible."

    expected = "expected returns are not possible."

    output, _, _ = await stream_text(
        assembler,
        text,
        chunk_size=100,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 10
# Phrase at end
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_phrase_at_end(assembler):

    text = (
        "Mutual funds never provide "
        "Guaranteed returns"
    )

    expected = (
        "Mutual funds never provide "
        "expected returns"
    )

    output, _, _ = await stream_text(
        assembler,
        text,
        chunk_size=100,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 11
# Finalize should flush buffer
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_finalize_flushes_buffer(assembler):

    state = StreamState(
        request=ProcessingRequest(text="")
    )

    result = await assembler.process_chunk(
        state,
        "Guaranteed",
        
    )

    assert result.chunk == ""

    final = await assembler.process_chunk(
        state,
        " returns",
        
    )

    assert final.blocked is False

    end = await assembler.finalize(state)

    output = (
        result.chunk +
        final.chunk +
        end.chunk
    )

    assert output == "expected returns"
    assert state.buffer == ""


# -------------------------------------------------------------------------
# Test 12
# Empty input
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_empty_input(assembler):

    output, state, _ = await stream_text(
        assembler,
        "",
        chunk_size=10,
    )

    assert output == ""
    assert state.complete_response == ""
    assert state.buffer == ""


# -------------------------------------------------------------------------
# Test 13
# Empty chunks
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_empty_chunks(assembler):

    output, _, _ = await stream_chunks(
        assembler,
        [
            "",
            "",
            "",
        ],
    )

    assert output == ""


# -------------------------------------------------------------------------
# Test 14
# Multiple empty chunks between data
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_empty_chunks_between_content(assembler):

    output, _, _ = await stream_chunks(
        assembler,
        [
            "Guaranteed",
            "",
            "",
            " returns",
        ],
    )

    assert output == "expected returns"


# -------------------------------------------------------------------------
# Test 15
# Reject policy
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reject_phrase_blocks_stream(assembler):

    state = StreamState(
        request=ProcessingRequest(text="")
    )

    result = await assembler.process_chunk(
        state,
        "This is a SEBI approved investment.",
        
    )

    assert result.blocked
    assert state.blocked
    assert state.reason is not None


# -------------------------------------------------------------------------
# Test 16
# Reject across chunk boundary
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reject_phrase_split_chunks(assembler):

    state = StreamState(
        request=ProcessingRequest(text="")
    )

    await assembler.process_chunk(
        state,
        "This is a SEBI approved",
        
    )

    result = await assembler.process_chunk(
        state,
        " investment.",
        
    )

    assert result.blocked
    assert state.blocked


# -------------------------------------------------------------------------
# Test 17
# No duplicate output
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_duplicate_output(assembler):

    text = (
        "Guaranteed returns "
        "Guaranteed returns"
    )

    expected = (
        "expected returns "
        "expected returns"
    )

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=7,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 18
# Carry over must be empty after finalize
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_finalize_clears_buffer(assembler):

    text = (
        "Guaranteed returns"
    )

    _, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=4,
    )

    assert state.buffer == ""


# -------------------------------------------------------------------------
# Test 19
# Complete response equals emitted response
# -------------------------------------------------------------------------


# @pytest.mark.asyncio
# async def test_complete_response_matches_output(assembler):

#     text = (
#         "Guaranteed returns "
#         "Assured returns"
#     )

#     output, state, _ = await stream_text(
#         assembler,
#         text,
#         chunk_size=6,
#     )

#     assert output == state.complete_response


# -------------------------------------------------------------------------
# Test 20
# No missing characters
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_missing_characters(assembler):

    text = (
        "abcdefghijklmnopqrstuvwxyz "
        "Guaranteed returns "
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )

    expected = (
        "abcdefghijklmnopqrstuvwxyz "
        "expected returns "
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )

    output, _, _ = await stream_text(
        assembler,
        text,
        chunk_size=8,
    )

    assert output == expected

    # -------------------------------------------------------------------------
# Test 21
# Chunk sizes from 1 to 200
# -------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "chunk_size",
    [1, 2, 3, 5, 7, 10, 16, 25, 32, 50, 64, 100, 128, 200],
)
async def test_all_chunk_sizes(
    assembler,
    chunk_size,
):

    text = (
        "Guaranteed returns are impossible. "
        "Risk free investment should never be promised. "
        "Assured returns are misleading."
    )

    expected = (
        "expected returns are impossible. "
        "lower-risk investment should never be promised. "
        "potential return are misleading."
    )

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=chunk_size,
    )

    assert output == expected
    assert state.buffer == ""


# -------------------------------------------------------------------------
# Test 22
# Phrase crossing many tiny chunks
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_phrase_crosses_many_chunks(assembler):

    chunks = [
        "Gu",
        "ar",
        "an",
        "te",
        "ed",
        " ",
        "re",
        "tu",
        "rn",
        "s",
    ]

    output, _, _ = await stream_chunks(
        assembler,
        chunks,
    )

    assert output == "expected returns"


# -------------------------------------------------------------------------
# Test 23
# Long stream with many replacements
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_long_stream_many_replacements(assembler):

    text = (
        (
            "Guaranteed returns. "
            "Risk free investment. "
            "Assured returns. "
        )
        * 100
    )

    expected = (
        (
            "expected returns. "
            "lower-risk investment. "
            "potential return. "
        )
        * 100
    )

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=37,
    )

    assert output == expected
    assert len(state.findings) == 300


# -------------------------------------------------------------------------
# Test 24
# Random chunk sizes
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_random_chunk_sizes(assembler):

    original = (
        "Guaranteed returns are impossible. "
        "Risk free investment should never be promised. "
        "Assured returns are misleading. "
    ) * 20

    expected = (
        "expected returns are impossible. "
        "lower-risk investment should never be promised. "
        "potential return are misleading. "
    ) * 20

    for _ in range(100):

        chunks = []

        remaining = original

        while remaining:

            size = random.randint(1, 200)

            chunks.append(
                remaining[:size]
            )

            remaining = remaining[size:]

        output, state, _ = await stream_chunks(
            assembler,
            chunks,
        )

        assert output == expected
        assert state.buffer == ""


# -------------------------------------------------------------------------
# Test 25
# Large Gemma-style chunks
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_large_gemma_chunks(assembler):

    paragraph = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Guaranteed returns are not permitted. "
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem. "
        "Risk free investment claims are prohibited. "
        "Assured returns should never be used. "
    )

    text = paragraph * 25

    expected = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "expected returns are not permitted. "
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem. "
        "lower-risk investment claims are prohibited. "
        "potential return should never be used. "
    ) * 25

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=200,
    )

    assert output == expected
    assert state.buffer == ""


# -------------------------------------------------------------------------
# Test 26
# Multiple replacements inside same context window
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_multiple_replacements_same_window(assembler):

    text = (
        "Guaranteed returns "
        "Guaranteed returns "
        "Guaranteed returns "
        "Guaranteed returns"
    )

    expected = (
        "expected returns "
        "expected returns "
        "expected returns "
        "expected returns"
    )

    output, _, _ = await stream_text(
        assembler,
        text,
        chunk_size=300,
    )

    assert output == expected


# -------------------------------------------------------------------------
# Test 27
# Stream one character at a time (stress)
# -------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_character_stream_stress(assembler):

    text = (
        (
            "Guaranteed returns. "
            "Risk free investment. "
            "Assured returns. "
        )
        * 30
    )

    expected = (
        (
            "expected returns. "
            "lower-risk investment. "
            "potential return. "
        )
        * 30
    )

    output, state, _ = await stream_text(
        assembler,
        text,
        chunk_size=1,
    )

    assert output == expected