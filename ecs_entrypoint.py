import os
import asyncio

from ingestion.bootstrap.ingestion_container import IngestionContainer
from app.core.database import SessionLocal
from app.core.config import settings
import psycopg

def main():
    print("HOST:", settings.POSTGRES_HOST)
    print("PORT:", settings.POSTGRES_PORT)
    print("DB:", settings.POSTGRES_DB)
    print("USER:", settings.POSTGRES_USER)

    try:
        conn = psycopg.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            dbname=settings.POSTGRES_DB,
            connect_timeout=10,
            sslmode="require"  # try this first
        )

        print("POSTGRES CONNECTION SUCCESS")
        conn.close()

    except Exception as e:
        print("POSTGRES CONNECTION FAILED")
        print(repr(e))
        raise
    bucket = os.environ['BUCKET']
    key = os.environ['KEY']
    document_type = os.environ['DOCUMENT_TYPE']
    try:
        with SessionLocal() as db:
            pipeline = IngestionContainer.build(db)
            result = pipeline.run_from_s3(bucket=bucket, key=key, document_type=document_type)
            print(result)
    finally:
        db.close()


if __name__ == '__main__':
    main()

