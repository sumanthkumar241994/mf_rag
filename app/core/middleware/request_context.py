# app/core/middleware/request_context.py
"""
Request context variables for logging and tracing
"""

from contextvars import ContextVar

request_id_ctx = ContextVar[str]("request_id", default='-')
client_ip_ctx = ContextVar[str]("client_ip", default='-')