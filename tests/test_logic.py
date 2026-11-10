"""Unit tests for the pure logic. No OpenAI calls are made: the LLM is replaced by fakes."""
import pandas as pd
import pytest
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableGenerator, RunnableLambda

from devops_bot.constants import PROMPT_PATH, QUESTIONS_PATH
from devops_bot.logic import classify_score, generate_question, get_response, parse_score


@pytest.fixture
def questions():
    return pd.DataFrame({
        "Question": ["Q1", "Q2", "Q3", "Q4"],
        "Topic": ["Docker", "Docker", "Kubernetes", "CI/CD"],
        "Level": ["Beginner", "Advanced", "Beginner", "beginner"],
    })


# --- generate_question -------------------------------------------------------

def test_generate_question_filters_by_topic_and_level(questions):
    for _ in range(20):
        assert generate_question(questions, set(), topics=["Docker"], level="Beginner") == "Q1"


def test_generate_question_level_is_case_insensitive(questions):
    picked = {generate_question(questions, set(), topics=["CI/CD"], level="BEGINNER") for _ in range(10)}
    assert picked == {"Q4"}


def test_generate_question_skips_already_asked(questions):
    assert generate_question(questions, {"Q1", "Q3"}, level="Beginner") == "Q4"


def test_generate_question_returns_none_when_pool_exhausted(questions):
    assert generate_question(questions, {"Q1"}, topics=["Docker"], level="Beginner") is None


# --- parse_score / classify_score --------------------------------------------

@pytest.mark.parametrize("text, expected", [
    ("**Score:** 7/10\n**Feedback:** ...", 7),   # format requested by the prompt
    ("**Score: 7/10**", 7),                         # bold around the whole line
    ("Score: 10 / 10", 10),                            # spaces around the slash
    ("**Score** - 3/10", 3),
    ("**Score:** 0/10", 0),
])
def test_parse_score_accepts_format_variations(text, expected):
    assert parse_score(text) == expected


@pytest.mark.parametrize("text", [
    "CD stands for Continuous Delivery ...",   # follow-up explanation, no score
    "Score: 42/10",                            # out of range
    "",
])
def test_parse_score_returns_none_without_valid_score(text):
    assert parse_score(text) is None


@pytest.mark.parametrize("score, expected", [
    (10, "correct"), (8, "correct"), (7, "partial"), (4, "partial"), (3, "incorrect"), (1, "incorrect"),
])
def test_classify_score_thresholds(score, expected):
    assert classify_score(score) == expected


# --- get_response --------------------------------------------------------------

def test_get_response_fills_prompt_and_streams_reply():
    seen_prompts = []

    def fake_llm(prompt_value):
        seen_prompts.append(prompt_value.to_string())
        return AIMessage(content="**Score:** 9/10")

    template = "Question: {current_question}\nAnswer: {user_answer}"
    reply = "".join(get_response(template, "an orchestrator", "What is Kubernetes?", llm=RunnableLambda(fake_llm)))

    assert reply == "**Score:** 9/10"
    assert seen_prompts == ["Human: Question: What is Kubernetes?\nAnswer: an orchestrator"]


def test_get_response_turns_mid_stream_errors_into_message():
    def failing_stream(_input):
        yield AIMessage(content="partial ")
        raise RuntimeError("invalid api key")

    reply = "".join(get_response("{current_question} {user_answer}", "a", "q", llm=RunnableGenerator(failing_stream)))

    assert reply.startswith("partial ")
    assert "Error: invalid api key" in reply


def test_get_response_without_api_key_returns_error_message(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    reply = "".join(get_response("{current_question} {user_answer}", "a", "q"))
    assert reply.startswith("Error:")


# --- bundled data files --------------------------------------------------------

def test_prompt_template_has_required_placeholders():
    template = PROMPT_PATH.read_text(encoding="utf-8")
    assert "{current_question}" in template and "{user_answer}" in template


def test_question_bank_is_valid():
    df = pd.read_excel(QUESTIONS_PATH)
    assert {"Question", "Topic", "Level"} <= set(df.columns)
    assert not df["Question"].duplicated().any()
    assert set(df["Level"]) <= {"Beginner", "Intermediate", "Advanced"}
