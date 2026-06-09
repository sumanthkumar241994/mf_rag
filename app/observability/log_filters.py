# app/observability/log_filters.py

import logging
import re
from app.core.middleware.request_context import request_id_ctx, client_ip_ctx

class RequestContextFilter(logging.Filter):

    def filter(self, record):
        record.request_id = request_id_ctx.get()
        record.client_ip = client_ip_ctx.get()
        return True