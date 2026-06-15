#app/core/config/aws.py
import boto3

from .settings import settings


class AWS:
    def __init__(self) -> None:
        self.session = boto3.Session(
            aws_access_key_id=settings.AWS_SECRET_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    @property
    def bedrock_runtime(self):
        return self.session.client('bedrock-runtime')

    @property
    def s3(self):
        return self.session.client('s3')
