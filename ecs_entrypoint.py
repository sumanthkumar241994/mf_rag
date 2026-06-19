import os
import asyncio

from ingestion.bootstrap.ingestion_container import IngestionContainer
from app.core.database import SessionLocal

async def main():
    bucket = os.environ['BUCKET']
    key = os.environ['KEY']
    document_type = os.environ['DOCUMENT_TYPE']
    try:
        async with SessionLocal() as db:
            pipeline = IngestionContainer.build(db)
            result = pipeline.run_from_s3(bucket=bucket, key=key, document_type=document_type)
            print(result)
    finally:
        db.close()


if __name__ == '__main__':
    asyncio.run(main())

