from app.api.dependencies.orchestrator import get_orchestrator
from app.services.chat_service import ChatService
from fastapi import Depends


_service: ChatService | None = None

def get_chat_service() -> ChatService:
    global _service

    if _service is None:
        _service = ChatService(
            orchestrator=get_orchestrator()
        )

    return _service

