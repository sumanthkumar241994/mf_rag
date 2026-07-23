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


# from app.compliance.loader.policy_loader import PolicyLoader
# from app.compliance.repository.policy_repository import PolicyRepository
# from app.compliance.response.policy_executor import PolicyExecutor
# from app.compliance.response.streaming.processing_request import ProcessingRequest
# from app.compliance.response.streaming.stream_state import StreamState
# from app.compliance.response.streaming.streaming_response_assembler import StreamingResponseAssembler
# from app.compliance.response.validators.policy_validator import PolicyValidator


# async def main():
#     repository = PolicyRepository(PolicyLoader())

#     validator = PolicyValidator(repository)

#     request = ProcessingRequest(
#         text="This fund offers guaranteed returns."
#     )

#     print("=" * 80)
#     print("DIRECT VALIDATOR")
#     print("=" * 80)

#     result = await validator.process(request)

#     print("INPUT : ", request.text)
#     print("OUTPUT: ", result.request.text)
#     print("FINDINGS:", result.findings)

#     print()

#     executor = PolicyExecutor(
#         validators=[
#             validator
#         ]
#     )

#     print("=" * 80)
#     print("DIRECT EXECUTOR")
#     print("=" * 80)

#     result = await executor.execute(request)

#     print("INPUT : ", request.text)
#     print("OUTPUT: ", result.request.text)
#     print("BLOCK :", result.blocked)
#     print("FINDINGS:", result.findings)

#     print()

#     assembler = StreamingResponseAssembler(
#         executor=executor,
#     )

#     state = StreamState(
#         request = ProcessingRequest(
#             text="",
#         )
#     )

#     print("=" * 80)
#     print("STREAMING")
#     print("=" * 80)

#     chunks = [
#         "This ",
#         "fund ",
#         "offers ",
#         "guaranteed ",
#         "returns.",
#     ]

#     for chunk in chunks:

#         print(f"\nCHUNK: {chunk!r}")

#         result = await assembler.process_chunk(
#             state,
#             chunk,
#         )

#         print("BUFFER :", state.buffer)
#         print("OUTPUT :", result.chunk)
#         print("BLOCKED:", result.blocked)

#     final = await assembler.finalize(state)

#     print("\nFINAL")
#     print("OUTPUT :", final.chunk)
#     print("BUFFER :", state.buffer)


# import asyncio

# from app.langfuse.client import LangfuseClient
# from app.langfuse.services.trace_service import TraceService

# async def main():
#     trace = TraceService(LangfuseClient())
#     result = trace.get_trace("9819b2c20f719300b1fa713990f65ddd")
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
# from datetime import datetime

# from langfuse._client.environment_variables import LANGFUSE_TRACING_ENABLED

# from app.api.dependencies.evaluation import get_evaluation_service
# from app.langfuse.client import LangfuseClient, langfuse_client
# from app.langfuse.services.trace_service import TraceService
# from app.notifications.zapier_client import ZapierClient
# from app.quality.evaluation.evaluation_service import EvaluationService
# from app.quality.evaluation.issue_analyzer import IssueAnalyzer
# from app.quality.evaluation.models.evaluation_context import EvaluationContext
# from app.unit_of_work.conversation_uow import ConversationUnitOfWork
# from app.unit_of_work.conversation_uow_factory import ConversationUnitOfWorkFactory

# async def main():
#     conversation_id: str = 'dc4ff496-1a67-4772-8c09-88cc060cfa28'
#     assistant_message_id: str = '0735c5a4-b461-4d98-b0b1-329917c75891'
#     trace_id: str = '9819b2c20f719300b1fa713990f65ddd'

#     uow_factory=ConversationUnitOfWorkFactory()
#     analyzer = IssueAnalyzer()
#     zapier = ZapierClient()
#     service: EvaluationService = get_evaluation_service()

#     uow = await  uow_factory.create()

#     async with uow:

#         conversation = await uow.conversations.get_by_id(
#             conversation_id
#         )

#         assistant_message = await uow.messages.get_by_id(
#             assistant_message_id
#         )

#         user_message = await uow.messages.get_previous_user_message(conversation_id=conversation.id, sequence_number=assistant_message.sequence_number)

#     trace = TraceService(langfuse_client).get_trace(
#         trace_id
#     )

#     context = EvaluationContext(
#         evaluation_id=None,
#         conversation=conversation,
#         user_message=user_message,
#         assistant_message=assistant_message,
#         feedback=None,
#         trace=trace,
#         created_at=datetime.utcnow(),
#     )

#     result = await service.evaluate(context)
#     # event = await analyzer.analyze(context, result)
#     # try:
#     #     await zapier.notify(event)
#     # except Exception as ex:
#     #     print(str(ex))
#     # trace = TraceService(LangfuseClient())
#     # result = trace.get_trace("9819b2c20f719300b1fa713990f65ddd")
#     print(result)
    
# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio

from app.api.dependencies.feedback_insight import get_feedback_insight_service
from app.quality.feedback.feedback_insight_service import FeedbackInsightService
from app.unit_of_work.feedback_insight_uow_factory import FeedbackInsightUnitOfWorkFactory

async def main():
    # conversation_id: str = 'dc4ff496-1a67-4772-8c09-88cc060cfa28'
    # assistant_message_id: str = '0735c5a4-b461-4d98-b0b1-329917c75891'
    # trace_id: str = '9819b2c20f719300b1fa713990f65ddd'
    feedback_id: str = "0b7cef1b-d869-4696-a50e-941d5965ae85"
    uow_factory=FeedbackInsightUnitOfWorkFactory()
    service: FeedbackInsightService = get_feedback_insight_service()

    uow = await  uow_factory.create()

    async with uow:

       feedback = await uow.feedbacks.get_by_id(feedback_id=feedback_id)
       result = await service.process(feedback)
    # event = await analyzer.analyze(context, result)
    # try:
    #     await zapier.notify(event)
    # except Exception as ex:
    #     print(str(ex))
    # trace = TraceService(LangfuseClient())
    # result = trace.get_trace("9819b2c20f719300b1fa713990f65ddd")
    print(result)
    
if __name__ == "__main__":
    asyncio.run(main())