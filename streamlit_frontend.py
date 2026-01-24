import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread-1"}}

st.title("LangGraph Chatbot 🤖")

if "message_history" not in st.session_state:
    st.session_state.message_history = []

# Show previous messages
for msg in st.session_state.message_history:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])

user_input = st.chat_input("Type here...")

if user_input:
    # User message
    st.session_state.message_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.text(user_input)

    # Invoke graph
    result = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=CONFIG
    )

    ai_message = result["messages"][-1].content

    # Assistant message
    st.session_state.message_history.append(
        {"role": "assistant", "content": ai_message}
    )
    with st.chat_message("assistant"):
        st.text(ai_message)