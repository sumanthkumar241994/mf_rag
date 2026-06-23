import json
import asyncio

from app.core.config import settings

class BedrockEmbeddingClient:

    def __init__(self, bedrock_client):
        self.client = bedrock_client

    async def generate(
        self,
        text: str
    ) -> list[float]:
        payload = {
            "inputText": text
        }

        response = await asyncio.to_thread(self.client.invoke_model,
            modelId=settings.BEDROCK_EMBEDDING_MODEL,
            body=json.dumps(payload)
        )

        body = json.loads(response['body'].read())

        return body['embedding']

    