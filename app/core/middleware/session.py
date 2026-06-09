from tkinter import EW
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from typing import Callable
from app.core.database import AsyncSessionLocal

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        async with AsyncSessionLocal() as session:
            request.state.session = session
            response = await call_next(request)
            return response

def register_session_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware)