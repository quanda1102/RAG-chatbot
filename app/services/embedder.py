import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EmbedderService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    def create_embedding(self, text: str) -> list[float]:
        """Creates an embedding for the given text."""
        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding

embedder_service = EmbedderService()
