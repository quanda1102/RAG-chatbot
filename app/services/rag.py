from openai import OpenAI
from app.services.embedder import embedder_service
from app.services.qdrant_client import qdrant_service
from app.services.ai_memory import ai_memory
from app.config import my_config

class RAGService:
    def __init__(self):
        self.client = OpenAI(api_key=my_config.OPENAI_API_KEY)
        self.chat_model = my_config.CHAT_MODEL

    def ask(self, question: str) ->list[str]:
        """
        Asks a question to the RAG system.
        Returns the answer and the context used.
        """
        question_vector = embedder_service.create_embedding(question)

        context_documents = qdrant_service.search_documents(question_vector)
        context = "\n---\n".join(context_documents)
        return context_documents


rag_service = RAGService()
