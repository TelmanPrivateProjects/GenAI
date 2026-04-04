import random
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

def extract_question_from_history(history):
    for msg in reversed(history):
        if hasattr(msg, "content") and "question" in msg.content.lower():
            match = re.search(r"\*\*(.+?)\*\*", msg.content)
            return match.group(1).strip() if match else msg.content.strip()
    return "No specific question found."

def get_response(prompt_template, user_answer, current_question):
    try:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        llm = ChatOpenAI()
        chain = prompt | llm | StrOutputParser()
        return chain.stream({
            "current_question": current_question,
            "user_answer": user_answer,
        })
    except Exception as e:
        return iter([f"❌ Error: {str(e)}"])
