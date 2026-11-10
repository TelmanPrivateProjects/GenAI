"""End-to-end test of the Streamlit app with Streamlit's AppTest.

The OpenAI model is replaced by a fake that records every prompt and returns
canned replies, so the full chat flow is exercised without an API key.
"""
import pytest
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from streamlit.testing.v1 import AppTest

import devops_bot.logic as logic
from devops_bot.constants import PROJECT_ROOT

APP_PATH = str(PROJECT_ROOT / "app.py")


@pytest.fixture
def fake_llm(monkeypatch):
    """Patch the LLM factory; returns (prompts_seen, replies_queue)."""
    prompts, replies = [], []

    def respond(prompt_value):
        prompts.append(prompt_value.to_string())
        return AIMessage(content=replies.pop(0))

    monkeypatch.setattr(logic, "build_llm", lambda: RunnableLambda(respond))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    return prompts, replies


def question_context(prompt_text):
    """Return the question the prompt tells the LLM it is evaluating."""
    after = prompt_text.split("interview question:", 1)[1]
    return after.split("Here is the user", 1)[0].strip()


def sidebar_button(at, label):
    return next(b for b in at.sidebar.button if label in b.label)


def test_full_interview_flow(fake_llm):
    prompts, replies = fake_llm
    at = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not at.exception
    assert any("OPENAI_API_KEY" in w.value for w in at.warning)  # missing key is reported

    # 1. Ask a new question
    sidebar_button(at, "New Question").click().run()
    question = at.session_state["current_question"]
    assert question and question in at.chat_message[-1].markdown[0].value

    # 2. Answer it -> scored evaluation
    replies.append("**🔍 Score:** 9/10\n**🧠 Feedback:** Great.\n**✅ Model Answer:** ...")
    at.chat_input[0].set_value("My answer").run()
    assert question_context(prompts[-1]) == question
    assert at.session_state["total_count"] == 1
    assert at.session_state["correct_count"] == 1
    assert "Correct" in at.session_state["last_feedback"]

    # 3. Follow-up whose text and reply both mention "question": must still use the active question
    replies.append("Good question! CD means Continuous Delivery.")
    at.chat_input[0].set_value("I have a **quick question**: what is CD?").run()
    assert question_context(prompts[-1]) == question
    assert at.session_state["total_count"] == 1             # follow-ups are not scored
    assert "Score: 9/10" in at.session_state["last_feedback"]  # previous evaluation kept

    # 4. A partially correct answer in a slightly different score format
    replies.append("**🔍 Score: 5/10**\n**🧠 Feedback:** Missing details.")
    at.chat_input[0].set_value("Another answer").run()
    assert at.session_state["total_count"] == 2
    assert at.session_state["correct_count"] == 1
    assert "Partially Correct" in at.session_state["last_feedback"]
    assert not at.exception

    # 5. Start over resets everything
    sidebar_button(at, "Start Over").click().run()
    assert at.session_state["current_question"] is None
    assert at.session_state["total_count"] == 0
    assert len(at.chat_message) == 1


def test_answer_before_any_question_uses_neutral_context(fake_llm):
    prompts, replies = fake_llm
    at = AppTest.from_file(APP_PATH, default_timeout=30).run()

    replies.append("Please click **New Question** to start.")
    at.chat_input[0].set_value("hello").run()

    assert question_context(prompts[-1]) == "No specific question found."
    assert not at.exception
