# import asyncio

# from app.compliance.loader.policy_loader import PolicyLoader
# from app.compliance.repository.policy_repository import PolicyRepository
# from app.compliance.response.streaming.streaming_response_assembler import StreamingResponseAssembler
# from app.compliance.response.validators.policy_validator import PolicyValidator
# from tests.helpers.streaming_test_harness import StreamingTestHarness


# async def main():
#     repository = PolicyRepository(PolicyLoader())

#     executor = ResponseComplianceExecutor(
#         validators=[
#             PolicyValidator(repository),
#             PIIValidator(),
#         ]
#     )

#     assembler = StreamingResponseAssembler(
#         executor=executor,
#     )

#     harness = StreamingTestHarness(assembler)

#     # result = await harness.execute(
#     #     text="Guaranteed returns.",
#     #     chunk_size=5,
#     # )
#     result = await harness.execute(
#         text="Contact abc@gmail.com",
#         chunk_size=5,
#     )

#     print(result.output)
#     print(result.state.complete_response)
#     print(result.state.carry_over)
#     print(result.state.findings)


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio

from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.repository.policy_repository import PolicyRepository
from app.compliance.response.policy_executor import PolicyExecutor
from app.compliance.response.streaming.processing_request import ProcessingRequest
from app.compliance.response.streaming.stream_state import StreamState
from app.compliance.response.streaming.streaming_response_assembler import StreamingResponseAssembler
from app.compliance.response.validators.policy_validator import PolicyValidator


async def main():
    repository = PolicyRepository(PolicyLoader())

    validator = PolicyValidator(repository)

    request = ProcessingRequest(
        text="This fund offers guaranteed returns."
    )

    print("=" * 80)
    print("DIRECT VALIDATOR")
    print("=" * 80)

    result = await validator.process(request)

    print("INPUT : ", request.text)
    print("OUTPUT: ", result.request.text)
    print("FINDINGS:", result.findings)

    print()

    executor = PolicyExecutor(
        validators=[
            validator
        ]
    )

    print("=" * 80)
    print("DIRECT EXECUTOR")
    print("=" * 80)

    result = await executor.execute(request)

    print("INPUT : ", request.text)
    print("OUTPUT: ", result.request.text)
    print("BLOCK :", result.blocked)
    print("FINDINGS:", result.findings)

    print()

    assembler = StreamingResponseAssembler(
        executor=executor,
    )

    state = StreamState(
        request = ProcessingRequest(
            text="",
        )
    )

    print("=" * 80)
    print("STREAMING")
    print("=" * 80)

    chunks = [
        "This ",
        "fund ",
        "offers ",
        "guaranteed ",
        "returns.",
    ]

    for chunk in chunks:

        print(f"\nCHUNK: {chunk!r}")

        result = await assembler.process_chunk(
            state,
            chunk,
        )

        print("BUFFER :", state.buffer)
        print("OUTPUT :", result.chunk)
        print("BLOCKED:", result.blocked)

    final = await assembler.finalize(state)

    print("\nFINAL")
    print("OUTPUT :", final.chunk)
    print("BUFFER :", state.buffer)


if __name__ == "__main__":
    asyncio.run(main())