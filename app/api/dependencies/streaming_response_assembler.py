from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.repository.policy_repository import PolicyRepository
from app.compliance.response.policy_executor import PolicyExecutor
from app.compliance.response.streaming.streaming_response_assembler import StreamingResponseAssembler
from app.compliance.response.validators.policy_validator import PolicyValidator


def get_streaming_assembler() -> StreamingResponseAssembler:
    return StreamingResponseAssembler(
        executor=PolicyExecutor(
            validators=[
                PolicyValidator(PolicyRepository(PolicyLoader()))
            ]
        )
    )