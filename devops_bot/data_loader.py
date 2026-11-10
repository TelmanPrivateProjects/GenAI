import streamlit as st
import pandas as pd

@st.cache_data
def load_prompt(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

@st.cache_data
def load_questions(path):
    try:
        df = pd.read_excel(path)
        required_columns = {"Question", "Topic", "Level"}
        if not required_columns.issubset(df.columns):
            st.error(f"❌ The Excel file must contain the columns: {required_columns}")
            return pd.DataFrame(columns=list(required_columns))
        return df
    except FileNotFoundError:
        st.error("❌ Excel file not found.")
        return pd.DataFrame(columns=["Question", "Topic", "Level"])
    except Exception as e:
        st.error(f"❌ Error loading questions: {str(e)}")
        return pd.DataFrame(columns=["Question", "Topic", "Level"])
