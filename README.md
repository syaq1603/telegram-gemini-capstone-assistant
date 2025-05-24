# 💼 **FIN ADVISOR** (Web + Telegram Bot)

This project is a **financial assistant** powered by **Google Gemini**, accessible via both a **Flask web interface** and a **Telegram bot**.

### Users can:
- 📊 Ask finance-related questions (markets, economics, investing).
- 📎 Upload PDFs, CSVs, and image files for document analysis.
- 💬 Receive contextual AI-generated responses.
- 🧾 Type "generate PDF" (via web) to export Gemini's reply.
- 🔒 Use the Telegram bot to chat with Gemini on the go.

---

## 🚀 How to Use

### 🖥️ Web Interface
1. Visit the Flask web app.
2. Enter your name to begin a session.
3. Ask a financial question or upload a document.
4. View the extracted content and Gemini’s response.

### 💬 Telegram Bot
1. Open Telegram and search for your bot (e.g., `@your_bot_name`).
2. Send a message like:  
   > What is inflation?
3. Or upload a document (PDF, CSV, or image).
4. The bot replies with an AI-generated financial answer.

> Telegram handles both text and file input, routed through a **webhook**.

---

## 🧱 Frontend & Backend Overview

### 🎨 Frontend (Web Interface)
- **HTML + Jinja2 templates**.
- Pages include:
  - `index.html`, `main.html`
  - `gemini.html` (ask/upload)
  - `gemini_reply.html` (response view)
  - `logs.html`, `del_logs.html`, `telegram.html`

### 🧠 Backend (Shared)
- **Flask app**: Handles routes, sessions, file uploads, and logs.
- **Telegram webhook**: Configured to receive messages and file uploads.
- **Google Gemini API**: Processes both questions and file content.
- **SQLite**: Stores session details in `user.db`.

---

## ⚙️ Requirements

- Python 3.8+
- A **Telegram bot token** (via [@BotFather](https://t.me/botfather)).
- **Google Gemini API key**.

### Install dependencies

```bash
pip install -r requirements.txt

```
## File Structure
fin_advisor/
├── app.py
├── bot.py
├── assistant.py
├── handler.py
├── document_loader.py
├── requirements.txt
├── Procfile
├── .env
├── templates/
│   ├── index.html
│   ├── gemini.html
│   ├── gemini_reply.html
│   ├── logs.html
│   ├── del_logs.html
│   ├── telegram.html
│   └── main.html
