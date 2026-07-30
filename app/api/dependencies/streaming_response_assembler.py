from app.api.dependencies.policy_repository import get_policy_repository
from app.compliance.loader.policy_loader import PolicyLoader
from app.compliance.repository.policy_repository import PolicyRepository
from app.compliance.response.policy_executor import PolicyExecutor
from app.compliance.response.streaming.streaming_response_assembler import StreamingResponseAssembler
from app.compliance.response.validators.policy_validator import PolicyValidator


_streaming_assembler: StreamingResponseAssembler | None = None

def get_streaming_assembler() -> StreamingResponseAssembler:
    global _streaming_assembler

    if _streaming_assembler is None:
        _streaming_assembler = StreamingResponseAssembler(
            executor=PolicyExecutor(
                validators=[
                    PolicyValidator(
                        get_policy_repository()
                    )
                ]
            )
        )

    return _streaming_assembler