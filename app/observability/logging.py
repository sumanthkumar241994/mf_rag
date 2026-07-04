import logging
from app.observability.log_filters import RequestContextFilter

def setup_logging():
    formatter = logging.Formatter('[%(asctime)s %(correlation_id)s %(client_ip)s '
        '%(module)s:%(lineno)d] %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(RequestContextFilter())

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

