import json

from botocore.client import BaseClient

from ingestion.contracts import EmbeddingProvider


class BedrockEmebddingGenerator(EmbeddingProvider):
    MODEL_ID = 'amazon.titan-embed-text-v2:0'

    def __init__(self, bedrock_client: BaseClient):
        self._client = bedrock_client

    def generate(self, text: str) -> list[float]:
        body = {
            "inputText": text
        }

        response = self._client.invoke_model(
            modelId = self.MODEL_ID,
            body = json.dumps(body),
            contentType='Application/json',
            accept='Application/json'
        )

        response_body = json.loads(response['body'].read())

        return response_body['embedding']
    
    def generate_batch(self, texts: list[str]) -> list[list[float]]:
        return super().generate_batch(texts)