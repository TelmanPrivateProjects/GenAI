import os
import random
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from devops_bot.constants import CORRECT_THRESHOLD, DEFAULT_MODEL, PARTIAL_THRESHOLD

# Matches "**🔍 Score:** 7/10" as well as small format variations the LLM may
# produce, e.g. "**🔍 Score: 7/10**", "Score: 7 / 10" or "Score - 10/10".
SCORE_PATTERN = re.compile(r"Score\W{0,6}?(\d{1,2})\s*/\s*10", re.IGNORECASE)


def generate_question(df, asked, topics=None, level=None):
    df = df.copy()
    if topics:
        df = df[df["Topic"].isin(topics)]
    if level:
        df = df[df["Level"].str.lower() == level.lower()]
    df = df[~df["Question"].isin(asked)]

    if df.empty:
        return None
    return random.choice(df["Question"].tolist())


def parse_score(response_text):
    """Return the 0-10 score from an evaluation response, or None if there is none."""
    match = SCORE_PATTERN.search(response_text)
    if not match:
        return None
    score = int(match.group(1))
    return score if 0 <= score <= 10 else None


def classify_score(score):
    """Map a score to one of: 'correct', 'partial', 'incorrect'."""
    if score >= CORRECT_THRESHOLD:
        return "correct"
    if score >= PARTIAL_THRESHOLD:
        return "partial"
    return "incorrect"


def build_llm():
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL") or DEFAULT_MODEL)


def get_response(prompt_template, user_answer, current_question, llm=None):
    """Stream the coach's reply chunk by chunk.

    Errors are turned into a chat message instead of crashing the app. This
    covers errors raised while the stream is consumed (e.g. an invalid API key
    or a network failure), not only errors raised while building the chain.
    """
    try:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | (llm or build_llm()) | StrOutputParser()
        yield from chain.stream({
            "current_question": current_question,
            "user_answer": user_answer,
        })
    except Exception as e:
        yield f"❌ Error: {str(e)}"
