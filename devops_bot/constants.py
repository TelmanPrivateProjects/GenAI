from pathlib import Path

# --- Paths (resolved relative to the project root, so the app works from any cwd) ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = PROJECT_ROOT / "data" / "devops_questions.xlsx"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "interview_coach.txt"

# --- LLM settings ---
# Override with the OPENAI_MODEL environment variable (see .env.example).
DEFAULT_MODEL = "gpt-4o-mini"

# --- Scoring thresholds (score is 1-10) ---
CORRECT_THRESHOLD = 8   # score >= 8  -> Correct
PARTIAL_THRESHOLD = 4   # score >= 4  -> Partially Correct, otherwise Incorrect

NO_QUESTION_CONTEXT = "No specific question found."

WELCOME_MESSAGE = """
**Welcome to the DevOps Interview Practice Bot!**

This assistant will help you prepare for DevOps interviews by:

- Asking you technical DevOps questions  
- Giving helpful, structured feedback on your answers  
- Scoring your answers from 1 to 10  
- Showing a model answer for every question  
- Tracking your progress in the sidebar

---
To begin:
1. Select a topic and difficulty level from the left panel  
2. Click **"New Question"**  
3. Type your answer in the chat box and hit Enter!

You can restart or reset your progress anytime using the buttons in the sidebar.

Ready? Let’s get started!

"""
