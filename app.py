import os

import streamlit as st
from dotenv import load_dotenv

from devops_bot.constants import PROJECT_ROOT, WELCOME_MESSAGE
from devops_bot.state import initialize_session_state
from devops_bot.ui import handle_user_input, render_chat, render_sidebar

# Load environment variables from the project's .env file
load_dotenv(PROJECT_ROOT / ".env")

# App config
st.set_page_config(page_title="DevOps Interview")
st.title("DevOps Interview Practice Bot")

if not os.getenv("OPENAI_API_KEY"):
    st.warning(
        "`OPENAI_API_KEY` is not set. Copy `.env.example` to `.env` and add your key "
        "to get AI feedback on your answers."
    )

# Initialize session state (first time load)
initialize_session_state(WELCOME_MESSAGE)

# --- Render UI ---
render_sidebar()
render_chat()
handle_user_input()
