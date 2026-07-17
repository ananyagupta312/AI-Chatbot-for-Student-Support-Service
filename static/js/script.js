/* =========================================================
   AI Chatbot for Student Support Services — Frontend Logic
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  // -------------------------------------------------------
  // Dark mode toggle (works on both home and chat pages)
  // -------------------------------------------------------
  const themeToggleBtn = document.getElementById("theme-toggle");

  // Apply saved theme preference on page load
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    if (themeToggleBtn) themeToggleBtn.textContent = "☀️";
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
      const isDark = document.body.classList.contains("dark-mode");
      themeToggleBtn.textContent = isDark ? "☀️" : "🌙";
      localStorage.setItem("theme", isDark ? "dark" : "light");
    });
  }

  // -------------------------------------------------------
  // Chat page logic (only runs if chat elements exist)
  // -------------------------------------------------------
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const typingIndicator = document.getElementById("typing-indicator");
  const clearChatBtn = document.getElementById("clear-chat-btn");
  const suggestionChips = document.querySelectorAll(".suggestion-chip");

  // If we're not on the chat page, stop here.
  if (!chatBox || !userInput || !sendBtn) return;

  /**
   * Returns the current time formatted like "10:45 AM"
   */
  function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  /**
   * Appends a chat bubble to the chat box.
   * @param {string} text - message content
   * @param {"user"|"bot"} sender - who sent the message
   */
  function appendMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    // Use textContent for safety (avoids HTML injection), then add timestamp
    const textNode = document.createTextNode(text);
    bubble.appendChild(textNode);

    const timeSpan = document.createElement("div");
    timeSpan.classList.add("timestamp");
    timeSpan.textContent = getCurrentTime();
    bubble.appendChild(timeSpan);

    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);

    scrollToBottom();
  }

  /** Scrolls the chat box to the latest message */
  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  /** Shows the animated "typing..." indicator */
  function showTyping() {
    typingIndicator.style.display = "block";
    scrollToBottom();
  }

  /** Hides the typing indicator */
  function hideTyping() {
    typingIndicator.style.display = "none";
  }

  /**
   * Sends the user's message to the Flask backend (/ask route)
   * and displays the AI's reply once it arrives.
   */
  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Show the user's message immediately
    appendMessage(message, "user");
    userInput.value = "";
    userInput.focus();

    // Hide suggestion chips after first message
    const suggestionsBar = document.getElementById("suggested-questions");
    if (suggestionsBar) suggestionsBar.style.display = "none";

    showTyping();
    sendBtn.disabled = true;

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }

      const data = await response.json();
      hideTyping();
      appendMessage(data.response || "Sorry, I didn't get that. Please try again.", "bot");

    } catch (error) {
      console.error("Error contacting the chatbot API:", error);
      hideTyping();
      appendMessage(
        "⚠️ Sorry, I couldn't connect to the server. Please check your connection and try again.",
        "bot"
      );
    } finally {
      sendBtn.disabled = false;
    }
  }

  // Send button click
  sendBtn.addEventListener("click", sendMessage);

  // Enter key sends the message (Shift+Enter could be used for newline if needed)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  // Suggested question chips auto-fill and send
  suggestionChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      userInput.value = chip.textContent;
      sendMessage();
    });
  });

  // Clear chat button
  if (clearChatBtn) {
    clearChatBtn.addEventListener("click", () => {
      chatBox.innerHTML = "";
      appendMessage(
        "👋 Hi again! Ask me anything about admissions, scholarships, courses, fees, hostel, placements, and more.",
        "bot"
      );
      const suggestionsBar = document.getElementById("suggested-questions");
      if (suggestionsBar) suggestionsBar.style.display = "flex";
    });
  }

  // Set timestamp on the initial welcome message
  const initialTimestamp = document.querySelector(".bot-message .timestamp");
  if (initialTimestamp) {
    initialTimestamp.textContent = getCurrentTime();
  }
});
