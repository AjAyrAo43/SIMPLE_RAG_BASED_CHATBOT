from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
import os

# Load .env file
load_dotenv()

# Read API key safely
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")

# Initialize model
model = ChatMistralAI(
    model="mistral-small",
    mistral_api_key=MISTRAL_API_KEY
)

# State definition
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Node
def chat_node(state: ChatState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# Checkpointer (memory)
checkpointer = InMemorySaver()

# Graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile
chatbot = graph.compile(checkpointer=checkpointer)

