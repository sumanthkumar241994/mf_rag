from fastapi import Depends, Request

from app.dtos.request_context import RequestContext

async def build_request_context(request: Request, chat_request: RequestContext) -> RequestContext:
    chat_request.customer_id = request.state.customer_id
    return chat_request