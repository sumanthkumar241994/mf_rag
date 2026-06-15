import hashlib


class ChunkHasher:

    def generate(self, content: str) -> str:
        """
        Generate a deterministic SHA256 hash for normalized chunk content.
        """
        return hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()