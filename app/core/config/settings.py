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

settings = Settings()