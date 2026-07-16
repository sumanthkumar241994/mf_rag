from app.ai.guardrails.deterministic.validators.domain_validator import DomainValidator
from app.ai.guardrails.deterministic.validators.input_size_validator import (
    InputSizeValidator,
)
from app.ai.guardrails.deterministic.validators.prompt_injection_validator import (
    PromptInjectionValidator,
)
from app.ai.guardrails.deterministic.validators.abuse_validator import (
    AbuseValidator,
)


from app.ai.guardrails.guardrail_service import GuardRailService
from app.ai.guardrails.llm.llm_guard_parser import LLMGuardParser
from app.ai.guardrails.llm.llm_guard_prompt_builder import LLMGuardPromptBuilder
from app.ai.guardrails.llm.llm_guard_service import LLMGuardService
from app.ai.guardrails.llm.llm_validator import LLMGuardValidator
from app.llm_gateway.llm_gateway import LLMGateway



class GuardRailComposition:

    def __init__(
        self,
        llm_gateway: LLMGateway,
    ):

        self.prompt_builder = LLMGuardPromptBuilder()
        self.parser = LLMGuardParser()
        self.validator = LLMGuardValidator()

        self.llm_guard_service = LLMGuardService(
            prompt_builder=self.prompt_builder,
            llm_gateway=llm_gateway,
            parser=self.parser,
            validator=self.validator,
        )

        self.guardrail_service = GuardRailService(
            validators=[
                InputSizeValidator(),
                PromptInjectionValidator(),
                AbuseValidator(),
                DomainValidator(),
            ],
            llm_guard_service=self.llm_guard_service,
        )