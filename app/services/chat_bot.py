from agents import Agent, Runner, Trace, function_tool
from app.services.rag import rag_service
from app.config import my_config
import json

@function_tool
def rag_tool(question: str) -> list[str]:
    return rag_service.ask(question)
 

agent = Agent(
    name="ChatBot",
    tools=[rag_tool],
    instructions=my_config.SYSTEM_PROMPT,
    model=my_config.CHAT_MODEL,
)


