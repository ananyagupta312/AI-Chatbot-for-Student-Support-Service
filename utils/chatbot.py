"""
chatbot.py
-----------
Helper module that talks to the Google Gemini API.

This file is intentionally kept simple and well commented so that
students can easily understand how the AI integration works.
"""

import os
import google.generativeai as genai

# ---------------------------------------------------------------------------
# System prompt: this tells Gemini HOW to behave.
# It restricts the bot to only answer student-support related questions.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an AI Student Support Assistant for a college.

Your job is to help students with questions related to:
- Admissions
- Scholarships
- Courses
- Fees
- Hostel
- Placements
- Library
- Exam Schedule
- Attendance
- Faculty
- Events
- Internships
- Career Guidance
- Contact Details

Rules you must always follow:
1. Answer politely and in a friendly, helpful tone.
2. Keep answers SHORT and CLEAR (2-5 sentences, use bullet points when helpful).
3. Only answer questions related to student support services listed above.
4. If the question is NOT related to student support services
   (for example, general knowledge, coding help, entertainment, etc.),
   politely reply with exactly:
   "I can only answer questions related to student support services."
5. If you don't have exact details (like real fee numbers), give a
   helpful general answer and suggest the student contact the
   admin office / college website for exact figures.
"""

# Name of the Gemini model to use.
# gemini-2.5-flash is fast, free-tier friendly, and great for chatbots.
MODEL_NAME = "gemini-3.5-flash"

# Module level variable that will hold the loaded model instance.
_model = None


def load_model():
    """
    Configures the Gemini SDK with our API key and loads the model.
    This is called once when the Flask app starts.

    Returns:
        A GenerativeModel instance ready to generate responses.
    """
    global _model

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Please add it to your .env file."
        )

    # Configure the Gemini SDK with our API key
    genai.configure(api_key=api_key)

    # Create the model with our system instruction (system prompt)
    _model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
    )

    return _model


def get_model():
    """
    Returns the already-loaded model, loading it first if needed.
    Having this helper avoids re-loading the model on every request.
    """
    global _model
    if _model is None:
        _model = load_model()
    return _model


def generate_response(user_message: str) -> str:
    """
    Sends the user's message to Gemini and returns the AI's reply.

    Args:
        user_message (str): The question typed by the student.

    Returns:
        str: The chatbot's reply as plain text.
    """
    # Basic input validation
    if not user_message or not user_message.strip():
        return "Please type a question so I can help you."

    try:
        model = get_model()

        # Ask Gemini to generate a response for the user's message
        result = model.generate_content(user_message)

        # Extract plain text from the response
        reply_text = result.text.strip() if result and result.text else None

        if not reply_text:
            return "Sorry, I couldn't generate a response. Please try again."

        return reply_text

    except Exception as error:
        # Catch any API / network errors so the app never crashes
        print(f"[chatbot.py] Error while generating response: {error}")
        return (
            "Sorry, something went wrong while contacting the AI service. "
            "Please try again in a moment."
        )
