from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Mutual fund Agentic Search Engine"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Agentic search for mutual funds"
    APP_DOCS_URL: str = "/docs"
    APP_REDOC_URL: str = "/redoc"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    JWT_SALT: str

    AWS_SECRET_ACCESS_KEY: str
    AWS_SECRET_KEY_ID: str
    AWS_REGION: str


    BEDROCK_TITAN_EMBEDDING_MODEL_ID: str
    BEDROCK_GEMMA_MODEL_ID : str = ''

    BEDROCK_CLAUDE_HAIKU_MODEL_ID: str 
    BEDROCK_CLAUDE_SONNET_MODEL_ID: str


    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_BASE_URL: str

    HIGH_PRIORITY_QUEUE_URL: str
    MEDIUM_PRIORITY_QUEUE_URL: str
    LOW_PRIORITY_QUEUE_URL: str

    MF_API_BASE_URL: str
    X_KARAT_API_KEY: str
    X_API_KEY: str

    REDIS_URL: str

    CONVERSATION_SUMMARY_INTERVAL: int = 1

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    @property
    def ASYNC_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
            )
    
    @property
    def SYNC_DATABASE_URL(self):
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @property
    def POSTGRES_CHECKPOINT_URL(self):
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

settings = Settings()