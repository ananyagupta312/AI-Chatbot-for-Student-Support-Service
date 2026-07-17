# 🎓 AI Chatbot for Student Support Services

An end-to-end, beginner-friendly **Generative AI course project** — a web-based chatbot
that helps students get instant answers about admissions, scholarships, courses, fees,
hostel, placements, library, exams, and more. Built with **Flask** and powered by the
**Google Gemini API**.

---

## 📖 Project Description

Colleges receive hundreds of repetitive queries from students every day. This project
solves that problem with a simple AI-powered chatbot that:

- Answers common student support questions instantly
- Politely refuses to answer questions unrelated to student support
- Runs entirely in the browser with a clean, modern chat interface
- Requires no database — it's a lightweight, stateless Flask app

---

## ✨ Features

- 🏠 Attractive landing page with a "Start Chat" button
- 💬 Real chatbot interface with chat bubbles (user right, bot left)
- 🤖 Google Gemini API integration with a custom system prompt
- ⌨️ Send messages with the **Enter** key or the send button
- ⏳ Animated "typing..." indicator while waiting for a reply
- 📜 Auto-scroll to the latest message
- 🌗 Dark mode toggle
- 🧹 Clear chat button
- 🕒 Message timestamps
- 💡 Suggested question chips for quick starts
- 📱 Fully responsive, mobile-friendly design
- 🛡️ Graceful error handling on both frontend and backend

---

## 🛠️ Technologies Used

| Layer     | Technology                                  |
|-----------|----------------------------------------------|
| Frontend  | HTML5, CSS3 (Glassmorphism UI), JavaScript   |
| Backend   | Python, Flask                                |
| AI Model  | Google Gemini API (`gemini-2.5-flash`)       |
| Config    | python-dotenv (`.env` file for API key)      |
| Font      | Google Fonts — Poppins                       |

---

## 📁 Project Structure

```
AI-Student-Chatbot/
│
├── app.py                 # Main Flask application (routes)
├── requirements.txt        # Python dependencies
├── .env                     # Stores your Gemini API key (keep this secret!)
├── README.md
│
├── static/
│   ├── css/
│   │      style.css        # Modern glassmorphism styling
│   ├── js/
│   │      script.js        # Chat logic, fetch calls, dark mode, etc.
│   └── images/              # (optional) image assets
│
├── templates/
│      index.html            # Landing page
│      chat.html             # Chatbot interface
│
├── utils/
│      chatbot.py            # Gemini API helper (load_model, generate_response)
│
└── screenshots/             # Add your project screenshots here
```

---

## ⚙️ Installation & Setup

### 1. Clone / Download the project
Unzip the project folder and open it in **VS Code**.

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your Google Gemini API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key

### 5. Add your API key to `.env`

Open the `.env` file in the project root and replace the placeholder:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

⚠️ **Never share your `.env` file or commit it to a public GitHub repo.**

### 6. Run the application

```bash
python app.py
```

The app will start at:

```
http://127.0.0.1:5000/
```

Open that URL in your browser. Click **"Start Chat"** to begin chatting!

---

## 🧪 API Endpoints

| Method | Route   | Description                                  |
|--------|---------|-----------------------------------------------|
| GET    | `/`     | Renders the home / landing page               |
| GET    | `/chat` | Renders the chatbot interface                 |
| POST   | `/ask`  | Accepts `{ "message": "..." }` and returns `{ "response": "..." }` |

**Example request to `/ask`:**
```json
{
  "message": "What are the admission requirements?"
}
```

**Example response:**
```json
{
  "response": "Admission requirements typically include your previous academic transcripts, an entrance exam score, and a completed application form. Please check the official admissions page for exact criteria."
}
```

---

## 📷 Screenshots

> Add your own screenshots of the Home page and Chat page here after running the project.

```
screenshots/
  ├── home-page.png
  └── chat-page.png
```

---

## 🚀 Future Improvements

- Add user authentication and chat history persistence (database)
- Connect to real college data (fees, exam dates) via an API or database
- Add multi-language support
- Add voice input/output
- Deploy to a cloud platform (Render, Railway, Azure, etc.)
- Add analytics dashboard for the most-asked questions

---

## 👩‍💻 Author's Note

This project was built as a **Generative AI course project** to demonstrate how to
integrate a Large Language Model (Google Gemini) into a full-stack web application
using Flask, with a clean and modular codebase suitable for learning purposes.

Enjoy building! 🎉
