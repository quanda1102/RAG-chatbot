from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.rag_schema import Question, Answer  
from app.services.rag import rag_service
from app.services.ai_memory import ai_memory
from agents import Runner, RawResponsesStreamEvent
from app.services.chat_bot import agent
import json
router = APIRouter()

@router.post("/rag/ask")
async def ask_question(question: Question):
    """
    Receives a question, processes it through the RAG pipeline,
    and returns a streaming SSE response.
    """
    async def generate_sse():
        try:
            last_conversations = ai_memory.get_last_n_conversations(question.session_id) or "Chưa có gì cả"
            print(last_conversations)
            ai_memory.save_user_input(question.session_id, question.question)
            
            # Use regular run with streaming callback
            full_response = ""
            
            def stream_callback(delta_text):
                nonlocal full_response
                full_response += delta_text
                return f"data: {delta_text}\n\n"
            
            # Get streamed result
            result = Runner.run_streamed(agent, input=f"Thông tin từ bộ nhớ: {last_conversations}\n\nCâu hỏi: {question.question}")
            
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event, RawResponsesStreamEvent):
                    # Check if the data has delta attribute for text content
                    if hasattr(event.data, 'delta'):
                        delta = event.data.delta
                        full_response += delta
                        
                        # Send only the text delta as SSE data
                        yield f"data: {delta}\n\n"
            
            # Save the complete response
            ai_memory.save_llm_response(question.session_id, full_response)
            
            # Send completion signal
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            # Send error as plain text
            yield f"data: Error: {str(e)}\n\n"
    
    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )
