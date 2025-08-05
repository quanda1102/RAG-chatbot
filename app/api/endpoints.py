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
            
            # Initialize streaming state
            full_response = ""
            
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'message': 'Starting response generation'})}\n\n"
            
            # Get streamed result
            result = Runner.run_streamed(agent, input=f"Thông tin từ bộ nhớ: {last_conversations}\n\nCâu hỏi: {question.question}")
            
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event, RawResponsesStreamEvent):
                    if hasattr(event.data, 'type'):
                        # Handle user-facing text content
                        if (hasattr(event.data, 'delta') and 
                            event.data.type == 'response.output_text.delta'):
                            
                            delta = event.data.delta
                            full_response += delta
                            
                            # Send character delta event
                            yield f"data: {json.dumps({'type': 'delta', 'content': delta})}\n\n"
                        
                        # Handle function call events
                        elif event.data.type == 'response.function_call_arguments.delta':
                            # Send function call delta event
                            function_delta = event.data.delta if hasattr(event.data, 'delta') else ""
                            yield f"data: {json.dumps({'type': 'function_call', 'content': function_delta})}\n\n"
                        
                        elif event.data.type == 'response.function_call_arguments.done':
                            # Send function call completion event
                            yield f"data: {json.dumps({'type': 'function_call_complete'})}\n\n"
            
            # Save the complete response
            ai_memory.save_llm_response(question.session_id, full_response)
            
            # Send completion event with full response
            yield f"data: {json.dumps({'type': 'complete', 'full_response': full_response})}\n\n"
            
        except Exception as e:
            # Send error event
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
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
