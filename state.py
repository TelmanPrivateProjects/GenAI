import streamlit as st
from langchain_core.messages import AIMessage

def initialize_session_state(welcome_message):
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("asked_questions", set())
    st.session_state.setdefault("correct_count", 0)
    st.session_state.setdefault("total_count", 0)
    st.session_state.setdefault("last_feedback", "")

    if not st.session_state.chat_history:
        st.session_state.chat_history.append(AIMessage(content=welcome_message))

def reset_all():
    st.session_state.chat_history = []
    st.session_state.asked_questions = set()
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.last_feedback = ""
