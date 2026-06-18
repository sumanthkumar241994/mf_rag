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


from nt import pipe
from ingestion.bootstrap.ingestion_container import IngestionContainer
from app.core.database import SessionLocal

db = SessionLocal()
try:
    pipeline = IngestionContainer.build(db)
    # pipeline = container.pipeline
    pipeline.run(file_path="/Users/sumanth/Downloads/1781088432492.pdf", s3_path="local-test")
finally:
    db.close()

