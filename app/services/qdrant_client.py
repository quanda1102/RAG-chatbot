import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv()

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"), 
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = os.getenv("COLLECTION_NAME", "Thông tư nghị định 01")
        self.top_k = int(os.getenv("TOP_K", 10))

    def search_documents(self, vector: list[float]) -> list[str]:
        """Searches for documents in Qdrant based on the given vector."""
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=self.top_k,
            with_payload=True
        )
        return [hit.payload.get("content", "") for hit in search_result]

qdrant_service = QdrantService()
