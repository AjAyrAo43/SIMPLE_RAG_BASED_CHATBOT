from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
import os
from langchain_core.messages import HumanMessage
import sqlite3

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

conn = sqlite3.connect(database = 'chatbot.db',check_same_thread=False)

# Checkpointer (memory)
checkpointer = SqliteSaver(conn = conn)

# Graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads =set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)




