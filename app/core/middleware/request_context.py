import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.middleware.request_context_vars import (correlation_id_ctx, client_ip_ctx)
from fastapi import FastAPI, Request, Response
from typing import Callable

class RequestContextMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        # add request id 
        correlation_id = str(uuid.uuid4().hex)
        correlation_token = correlation_id_ctx.set(correlation_id)
        #add client ip
        client_ip = request.client.host
        client_token = client_ip_ctx.set(client_ip)

        request.state.correlation_id = correlation_id
        request.state.client_ip = client_ip
        # calls the next middleware
        try:
            response = await call_next(request)
        finally:
            correlation_id_ctx.reset(correlation_token)
            client_ip_ctx.reset(client_token)

        response.headers['X-Correlation-ID'] = correlation_id

        return response

def register_request_context_middleware(app: FastAPI):
    app.add_middleware(RequestContextMiddleware)