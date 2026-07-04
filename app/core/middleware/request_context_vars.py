# app/core/middleware/request_context.py
"""
Request context variables for logging and tracing
"""

from contextvars import ContextVar

correlation_id_ctx = ContextVar[str]("correlation_id", default='-')
client_ip_ctx = ContextVar[str]("client_ip", default='-')
trace_id_ctx = ContextVar[str]("trace_id", default='-')