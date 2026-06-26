# app/workers/main.py

import asyncio

from app.langfuse.client import langfuse_client

from app.workers.bootstrap import get_event_worker
from app.events.models.event_priority import EventPriority

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

async def main():
    print("starting worker")
    worker = get_event_worker()

    try:
        print("worker created")
        await worker.start()
    finally:
        langfuse_client.flush()

if __name__ == '__main__':
    asyncio.run(main())