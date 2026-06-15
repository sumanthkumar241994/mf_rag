from pathlib import Path

from app.core.config.aws import AWS
from app.core.database import SessionLocal
from ingestion.bootstrap.ingestion_container import IngestionContainer

def run(bucket: str, key: str):
    db = SessionLocal()

    try:

        local_file = f"/tmp/{Path(key).name}"

        AWS().s3.download_file(bucket, key, local_file)

        pipeline = IngestionContainer.build(db)

        result = pipeline.run(file_path=local_file, s3_path=f"s3://{bucket}/{key}")
        print(result)

        return result
    finally:
        db.close()