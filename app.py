"""
app.py
------
Main Flask application for the AI Chatbot for Student Support Services.

Routes:
    GET  /       -> Home / landing page
    GET  /chat   -> Chatbot page
    POST /ask    -> Receives a student's message and returns the AI reply
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from utils.chatbot import generate_response, load_model

# ---------------------------------------------------------------------------
# Load environment variables from the .env file (this loads GEMINI_API_KEY)
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# Create the Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Load the Gemini model once when the server starts, so every request
# doesn't have to re-initialize it. If the API key is missing/invalid,
# we print a warning but still let the app run (the /ask route will
# show a friendly error to the user instead of crashing the server).
try:
    load_model()
    print("✅ Gemini model loaded successfully.")
except Exception as e:
    print(f"⚠️  Warning: Could not load Gemini model at startup: {e}")
    print("    Make sure GEMINI_API_KEY is set correctly in your .env file.")


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Renders the landing/home page."""
    return render_template("index.html")


@app.route("/chat")
def chat():
    """Renders the chatbot interface page."""
    return render_template("chat.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    Receives a JSON payload like:
        { "message": "What are the admission requirements?" }

    Returns a JSON payload like:
        { "response": "..." }
    """
    try:
        data = request.get_json(silent=True)

        if not data or "message" not in data:
            return jsonify({"response": "Invalid request. 'message' field is required."}), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please type a question so I can help you."}), 400

        # Call our Gemini helper function to get the AI's reply
        ai_reply = generate_response(user_message)

        return jsonify({"response": ai_reply}), 200

    except Exception as e:
        # Never let the server crash - always return a friendly JSON error
        print(f"[app.py] Error in /ask route: {e}")
        return jsonify({
            "response": "Sorry, something went wrong on our end. Please try again."
        }), 500


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=True gives helpful error messages during development.
    # Turn this off (debug=False) before deploying to production.
    app.run(debug=True, host="0.0.0.0", port=5000)
