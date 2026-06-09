import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.middleware.request_context import (request_id_ctx, client_ip_ctx)
from fastapi import FastAPI, Request, Response
from typing import Callable

class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        # add request id 
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)
        #add client ip
        client_ip = request.client.host
        client_ip_ctx.set(client_ip)
        # calls the next middleware
        response = await call_next(request)

        response.headers['X-Request-ID'] = request_id

        return response

def register_logging_middleware(app: FastAPI):
    app.add_middleware(LoggingMiddleware)