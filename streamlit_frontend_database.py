import streamlit as st
import uuid
from langGraph_database_backend import chatbot , retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage

# -------------------- Utils --------------------

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_thread"]:
        st.session_state["chat_thread"].append(thread_id)

def reset_chat():
    new_thread_id = generate_thread_id()
    st.session_state["thread_id"] = new_thread_id
    add_thread(new_thread_id)
    st.session_state["message_history"] = []

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    return state.values.get("messages", [])

# -------------------- Session State --------------------

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_thread" not in st.session_state:
    st.session_state["chat_thread"] = retrieve_all_threads()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

add_thread(st.session_state["thread_id"])

# -------------------- Sidebar --------------------

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for tid in st.session_state["chat_thread"][::-1]:
    if st.sidebar.button(tid):
        st.session_state["thread_id"] = tid

        messages = load_conversation(tid)
        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            else:
                continue

            temp_messages.append({
                "role": role,
                "content": msg.content
            })

        st.session_state["message_history"] = temp_messages

# -------------------- Chat History --------------------

for msg in st.session_state["message_history"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------- Chat Input --------------------

user_input = st.chat_input("Type your message...")

if user_input:
    # User message
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    CONFIG ={
        "configurable":{"thread_id":st.session_state["thread_id"]},
        "metadata":{
            "thread_id":st.session_state["thread_id"]
        },
        "run_name":"chat_turn"
    }
    # Assistant streaming (FIXED)
    assistant_text = ""

    with st.chat_message("assistant"):
        placeholder = st.empty()

        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages"
        ):
            assistant_text += message_chunk.content
            placeholder.markdown(assistant_text)

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": assistant_text
    })