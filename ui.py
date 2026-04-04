import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from data_loader import load_questions, load_prompt
from logic import generate_question, extract_question_from_history, get_response
from state import reset_all
from constants import WELCOME_MESSAGE
import streamlit as st
import re

QUESTIONS_DF = load_questions("data/devops_questions_full.xlsx")
PROMPT_TEMPLATE = load_prompt("prompt.txt")

def render_sidebar():
    with st.sidebar:
        # --- Enhanced Performance Tracking ---
        st.markdown("### 📊 Your Progress")

        correct = st.session_state.correct_count
        total = st.session_state.total_count
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        # Show emojis based on accuracy
        if accuracy >= 80:
            status_emoji = "🟢"
        elif accuracy >= 40:
            status_emoji = "🟡"
        else:
            status_emoji = "🔴"

        # Stylized box
        with st.container():
            st.markdown(f"""
            <div style='background-color:#2c2f36;padding:15px;border-radius:10px;border:1px solid #ddd'>
                <h4 style='margin-bottom:5px;'>📈 Score Summary</h4>
                <p style='margin:0'><strong>Total Answered:</strong> {total}</p>
                <p style='margin:0'><strong>Correct Answers:</strong> {correct}</p>
                <p style='margin:0'><strong>Accuracy:</strong> {accuracy:.1f}% {status_emoji}</p>
            </div>
            """, unsafe_allow_html=True)

        # Progress Bar
        st.markdown("### 🔵 Accuracy Level")
        st.progress(accuracy / 100)

        # Show last feedback
        if "last_feedback" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state["last_feedback"], unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### ⚙️ Customize Practice")
        selected_topics = st.multiselect("🧠 Topic Filter", sorted(QUESTIONS_DF["Topic"].unique().tolist()))
        selected_level = st.selectbox("🎯 Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

        if st.button("🔄 Start Over", use_container_width=True):
            reset_all()
            st.session_state.chat_history = [
                AIMessage(content=WELCOME_MESSAGE)]
            st.rerun()

        if st.button("🔁 Refresh Questions", use_container_width=True):
            st.session_state.asked_questions.clear()
            st.success("✅ Question pool has been reset!")

        st.markdown("---")

        if st.button("❓ New Question", use_container_width=True):
            question = generate_question(
                df=QUESTIONS_DF,
                asked=st.session_state.asked_questions,
                topics=selected_topics,
                level=selected_level
            )
            if question is None:
                st.session_state.chat_history.append(AIMessage(content="🚫 No more unique questions available for the selected filters."))
            else:
                st.session_state.asked_questions.add(question)
                st.session_state.chat_history.append(AIMessage(content=f"💡 Here’s your next question:\n\n**{question}**"))

def render_chat():
    for msg in st.session_state.chat_history:
        with st.chat_message("AI" if isinstance(msg, AIMessage) else "Human"):
            st.markdown(msg.content)

def handle_user_input():
    user_query = st.chat_input("Your answer...")
    if user_query is None:
        return

    if not user_query.strip():
        st.warning("⚠️ Please enter a non-empty answer.")
        return

    # Add human message
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    # Get current question
    current_question = extract_question_from_history(st.session_state.chat_history)

    # Get AI response
    full_response = ""
    response_stream = get_response(PROMPT_TEMPLATE, user_query, current_question)

    with st.chat_message("AI"):
        placeholder = st.empty()
        for chunk in response_stream:
            full_response += chunk
            placeholder.markdown(full_response, unsafe_allow_html=True)

    # Extract score
    score_match = re.search(r"\*\*🔍 Score:\*\* (\d+)/10", full_response)

    if score_match:
        score = int(score_match.group(1))
        st.session_state.total_count += 1

        if score >= 8:
            st.session_state.correct_count += 1
            feedback_label = "🟢 <span style='color:green'><strong>Correct</strong></span>"
        elif score >= 4:
            feedback_label = "🟡 <span style='color:orange'><strong>Partially Correct</strong></span>"
        else:
            feedback_label = "🔴 <span style='color:red'><strong>Incorrect</strong></span>"

        feedback_html = f"**Last Evaluation:** {feedback_label} (Score: {score}/10)"
        st.markdown(feedback_html, unsafe_allow_html=True)
        st.session_state["last_feedback"] = feedback_html

    else:
        st.session_state["last_feedback"] = "**Last Evaluation:** No score found in response."
    
    # Add AI message
    st.session_state.chat_history.append(AIMessage(content=full_response))