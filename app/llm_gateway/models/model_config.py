from dataclasses import dataclass

from app.llm_gateway.enums.provider import Provider


@dataclass(slots=True, frozen=True)
class ModelConfig:
    provider: Provider
    model_id: str