from langfuse import Langfuse

from app.core.config.settings import settings

# langfuse_client = Langfuse(
#     base_url=settings.LANGFUSE_BASE_URL,
#     public_key=settings.LANGFUSE_PUBLIC_KEY,
#     secret_key=settings.LANGFUSE_SECRET_KEY
# )

class LangfuseClient:
    def __init__(self) -> None:
        self._client = Langfuse(
            base_url=settings.LANGFUSE_BASE_URL,
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
        )
    
    @property
    def client(self):
        return self._client
    
langfuse_client = LangfuseClient()