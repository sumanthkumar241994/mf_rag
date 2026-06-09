# app/core/middleware/tracing.py

import time
import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)

class TracingMiddleware:

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, recieve, send):
        start = time.perf_counter()
        await self.app(scope, recieve,send)
        elapsed = time.perf_counter() - start

        logger.info(f"Request completed in {elapsed:.3f} seconds")
        

def register_tracing_middleware(app: FastAPI):
    app.add_middleware(TracingMiddleware)
