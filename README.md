# 💻 DevOps Interview Practice Bot

This is a modular **Streamlit** application that helps users practice for **DevOps interviews** by asking technical questions, evaluating answers with AI, and providing feedback with a score.

---

## 🚀 Features

- Ask randomized DevOps questions filtered by topic and difficulty
- Get AI-generated feedback and model answers
- Track your progress (correct answers, total answered, accuracy %)
- Interactive chat interface using Streamlit
- Easily extendable with modular structure

---

## 📁 Project Structure

```
devops_bot/
├── main.py                  # Streamlit entry point
├── ui.py                    # UI components (chat, sidebar)
├── state.py                 # Session state management
├── logic.py                 # Core logic for Q&A and evaluation
├── data_loader.py           # Load prompt and questions from file
├── constants.py             # Static texts (e.g., welcome message)
├── requirements.txt         # Python dependencies
├── prompt.txt               # LLM prompt template
├── .env                     # Environment variables
└── data/
    └── devops_questions_full.xlsx
└── .streamlit/
    └── config.toml

---

## ⚙️ Setup Instructions

1. **Create virtual environment and install requirements**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up your `.env` file** with your OpenAI key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Run the Streamlit app**

```bash
streamlit run main.py
```

---

## 📌 Dependencies

-   streamlit
-   openai
-   langchain
-   pandas
-   python-dotenv
-   langchain_openai
-   langchain_core
-   dotenv
-   openpyxl

---

## 🧠 Customization

- Add your own DevOps questions in `data/devops_questions_full.xlsx`
- Modify the prompt in `prompt.txt`
- Adjust scoring rules in `logic.py`

---

## 📜 License

MIT License © 2025
