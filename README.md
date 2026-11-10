# 💻 DevOps Interview Practice Bot

A **Streamlit** chat app that helps you prepare for **DevOps interviews**. It asks technical questions, evaluates your answers with an LLM (via **LangChain** + **OpenAI**), scores them from 1 to 10, shows a model answer and tracks your progress.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- **100 curated questions** across 10 topics: CI/CD, Git, Docker, Kubernetes, IaC, Configuration Management, Monitoring, Logging & Observability, DevSecOps and Cloud Platforms
- **3 difficulty levels** (Beginner, Intermediate, Advanced) with topic filters
- **AI evaluation**: score (1–10), constructive feedback, a model answer and a link to the official docs
- **Follow-up questions** ("What is CD?") are answered without being scored
- **Progress tracking**: answered, correct (score ≥ 8) and accuracy in the sidebar
- Streaming responses and a dark theme

---

## 🧭 How it works

```
 Sidebar: topic + level ──► generate_question() ──► question saved in session_state
                                                            │
 User answer ──► prompt (prompts/interview_coach.txt) ◄─────┘
                    │
                    ▼
        LangChain: prompt | ChatOpenAI | StrOutputParser  (streamed)
                    │
                    ▼
        parse_score() ──► classify_score() ──► sidebar progress
```

---

## 📁 Project structure

```
.
├── app.py                       # Streamlit entry point
├── devops_bot/
│   ├── constants.py             # Paths, model default, thresholds, welcome text
│   ├── data_loader.py           # Load prompt and question bank (cached)
│   ├── logic.py                 # Question selection, LLM call, score parsing
│   ├── state.py                 # Session state management
│   └── ui.py                    # Sidebar, chat and input handling
├── prompts/
│   └── interview_coach.txt      # LLM prompt template
├── data/
│   └── devops_questions.xlsx    # Question bank (Question, Topic, Level)
├── tests/                       # Unit + end-to-end tests (no API key needed)
├── .streamlit/config.toml       # Theme
├── .env.example                 # Environment variable template
├── requirements.txt
└── requirements-dev.txt
```

---

## ⚙️ Setup

1. **Create a virtual environment and install the dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure your OpenAI key**

   ```bash
   cp .env.example .env
   ```

   Then edit `.env`:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini        # optional
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

> Without an API key the app still starts and shows a warning. Answers return an error message instead of feedback.

---

## 🧪 Tests

The test suite does not call OpenAI. The LLM is replaced by a fake, so **no API key is needed**.

```bash
pip install -r requirements-dev.txt
pytest
```

- `tests/test_logic.py`: question filtering, score parsing (including format variations), score thresholds, prompt filling and error handling during streaming.
- `tests/test_app.py`: an end-to-end chat flow using Streamlit's `AppTest`. It covers asking a question, answering, a follow-up question, a second answer and starting over.

---

## 🧠 Customization

| What | Where |
|------|-------|
| Add or edit questions | `data/devops_questions.xlsx` (columns: `Question`, `Topic`, `Level`) |
| Change the coach's behavior or output format | `prompts/interview_coach.txt` |
| Switch the model | `OPENAI_MODEL` in `.env` |
| Adjust the "correct" / "partially correct" thresholds | `CORRECT_THRESHOLD` / `PARTIAL_THRESHOLD` in `devops_bot/constants.py` |

---

## 📜 License

[MIT](LICENSE) © 2025 Telman Huseynli
