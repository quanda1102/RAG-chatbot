from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.endpoints import router as api_router
import uvicorn
load_dotenv()

app = FastAPI(
    title="RAG Chatbot API",
    description="API for a RAG (Retrieval-Augmented Generation) Chatbot using Qdrant and OpenAI.",
    version="0.1.0",
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the RAG Chatbot API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)