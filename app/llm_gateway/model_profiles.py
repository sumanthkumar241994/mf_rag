

from app.core.config import settings
from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.enums.provider import Provider
from app.llm_gateway.models.model_config import ModelConfig


MODEL_PROFILES = {
    ModelProfile.GUARDRAIL: ModelConfig(
        provider=Provider.GEMMA,
        model_id=settings.BEDROCK_GEMMA_MODEL_ID,
    ),
    ModelProfile.JUDGE: ModelConfig(
        provider=Provider.GEMMA,
        model_id=settings.BEDROCK_GEMMA_MODEL_ID,
    ),
    ModelProfile.CHAT: ModelConfig(
        provider=Provider.GEMMA,
        model_id=settings.BEDROCK_GEMMA_MODEL_ID,
    ),
    ModelProfile.PLANNER: ModelConfig(
        provider=Provider.GEMMA,
        model_id=settings.BEDROCK_GEMMA_MODEL_ID,
    ),
    # ModelProfile.GUARDRAIL: ModelConfig(
    #     provider=Provider.GEMMA,
    #     model_id=settings.BEDROCK_GEMMA_MODEL_ID,
    # ),
    # ModelProfile.PLANNER: ModelConfig(
    #     provider=Provider.ANTHROPIC,
    #     model_id=settings.BEDROCK_CLAUDE_HAIKU_MODEL_ID,
    # ),
    ModelProfile.TITLE: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id=settings.BEDROCK_CLAUDE_HAIKU_MODEL_ID,
    ),
    ModelProfile.SUMMARY: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id=settings.BEDROCK_CLAUDE_HAIKU_MODEL_ID,
    ),
    ModelProfile.MEMORY: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id=settings.BEDROCK_CLAUDE_HAIKU_MODEL_ID,
    ),
    ModelProfile.REFLECTION: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id=settings.BEDROCK_CLAUDE_SONNET_MODEL_ID,
    ),
    ModelProfile.EVALUATION: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id=settings.BEDROCK_CLAUDE_SONNET_MODEL_ID,
    ),
    ModelProfile.EMBEDDING: ModelConfig(
        provider=Provider.TITAN,
        model_id=settings.BEDROCK_TITAN_EMBEDDING_MODEL_ID,
    ),
}