from fastapi import Depends, Request

from app.schemas.requests.chat import ChatRequest

async def build_chat_request(request: Request, chat_request: ChatRequest) -> ChatRequest:
    context = request.state.context
    chat_request.session_id = context.session_id
    chat_request.customer_id = context.customer_id

    return chat_request