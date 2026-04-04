import streamlit as st
from dotenv import load_dotenv
from constants import WELCOME_MESSAGE
from state import initialize_session_state
from ui import render_sidebar, render_chat, handle_user_input

# Load environment variables
load_dotenv()

# App config
st.set_page_config(page_title="DevOps Interview", page_icon="💻")
st.title("💻 DevOps Interview Practice Bot")

# Initialize session state (first time load)
initialize_session_state(WELCOME_MESSAGE)

# --- Render UI ---
render_sidebar()
render_chat()
handle_user_input()

