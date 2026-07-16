import json
import asyncio

from app.core.config import settings
from app.core.config.aws import AWS

class BedrockTitanEmbedding:

    def __init__(self):
        self.client = AWS().bedrock_runtime

    async def generate(
        self,
        text: str
    ) -> list[float]:
        payload = {
            "inputText": text
        }

        response = await asyncio.to_thread(self.client.invoke_model,
            modelId=settings.BEDROCK_TITAN_EMBEDDING_MODEL_ID,
            body=json.dumps(payload)
        )

        body = json.loads(response['body'].read())

        return body['embedding']

    