from pathlib import Path

from app.core.config.aws import AWS
from app.core.database import SessionLocal
from ingestion.bootstrap.ingestion_container import IngestionContainer


# Glue import the secrets from the secret manager and here is template

# import os
# import json
# import boto3

# client = boto3.client("secretsmanager")

# secret = client.get_secret_value(
#     SecretId="mf-ingestion-config"
# )

# config = json.loads(secret["SecretString"])

# for key, value in config.items():
#     os.environ[key] = str(value)

# #
# # ONLY NOW import application code
# #
# from ingestion.bootstrap.container import IngestionContainer
# from app.core.database import SessionLocal


# from awsglue.utils import getResolvedOptions
# import sys

# args = getResolvedOptions(
#     sys.argv,
#     ["bucket", "key"]
# )

# bucket = args["bucket"]
# key = args["key"]

# print(bucket)
# print(key)

# pipeline.run_from_s3(
#     bucket=bucket,
#     key=key
# )


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