from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from typing import Callable
from app.core.security.auth import extract_token, verify_token


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        token = extract_token(request)
        payload = verify_token(token=token)
        request.state.customer_uid = payload['user']
        return await call_next(request)

        
def register_authentication_middleware(app: FastAPI):
    app.add_middleware(AuthenticationMiddleware)