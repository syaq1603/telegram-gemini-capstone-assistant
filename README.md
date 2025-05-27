# 💼 **FINANCIAL ADVISOR** (Web + Telegram Bot)

An AI-powered financial assistant that integrates OpenAI for intelligent financial replies and connects with users through a Telegram bot. Built with Flask, this assistant can answer questions and analyze uploaded documents, deployed on Render.

### Users can:
- 📊 Ask finance-related questions (markets, economics, investing).
- 📎 Upload PDFs, CSVs, and image files for document analysis.
- 💬 Receive contextual AI-generated responses.
- 🧾 Type "generate PDF" (via web) to export Gemini's reply.
- 🔒 Use the Telegram bot to chat with Gemini on the go.

-------------------------------------------------------------------------------------------------

## 🚀 How to Use

### 🖥️ Web Interface
1. Visit the Flask web app.
2. Enter your name to begin a session.
3. Ask a financial question or upload a document.
4. View the extracted content and Gemini’s response.

### 💬 Telegram Bot
1. Open Telegram and search for your bot (e.g., `@ytiabotbot`).
2. Send a message like:  
   > What is inflation?
3. Or upload a document (PDF, CSV, or image).
4. The bot replies with an AI-generated financial answer.

> Telegram handles both text and file input, routed through a **webhook**.

### 🎨 Frontend (Web Interface)
Pages:

`` — Ask a question or upload a document

`` — Show AI response

`` — Manage Telegram bot

`` — View bot start/stop results

`` — Confirm log deletion

UI Features:

- Simple interface for typing questions

- Document upload form

- Navigation to bot control

### 🧠 Backend (Shared)
🖥️ Backend: Flask API (OpenAI + Telegram)

Key Features:

- Handles routes:

- / → Ask a financial question

- /analyze_file → Upload file for analysis

- /telegram → Webhook endpoint for Telegram bot

- /start_telegram / /stop_telegram → Bot control

- Uses OpenAI gpt-3.5-turbo for generating replies

- Logs user activity (optional)

Key Libraries:

Flask, requests, openai, python-docx, PyPDF2, pytesseract, pillow
-----------------------------------------------------------------

🤖 Telegram Bot Integration

Bot username: @tiabotbot

Webhook endpoint: /telegram

Accepts messages and replies using OpenAI

Deployed and secured via Render environment

Example:

User: hello
Bot: Hello! How can I assist you with finance today?

🚀 Deployment on Render

🔧 Setup:

Create a new Web Service on Render

Connect to GitHub repo

Add environment variables:

OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=...
WEBHOOK_URL=https://your-render-url.onrender.com

Start Command:

gunicorn app:app

🌍 Set Telegram Webhook

curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=<WEBHOOK_URL>/telegram"

📝 .env Template

OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=...
WEBHOOK_URL=https://your-render-url.onrender.com

**Never commit **`` to GitHub.

🧪 Testing & Logs

Use Render Logs for webhook requests

Print statements log:

Received messages

Chat IDs

OpenAI responses

## ⚙️ Requirements

- Python 3.8+
- A **Telegram bot token** (via [@BotFather](https://t.me/botfather)).
- **OPENAI_API_KEYy**.

### Install dependencies

```bash
pip install -r requirements.txt

```
## File Structure

telegram_gemini_capstone_assistant/
├── app.py                  # Main Flask app entry point
├── bot.py                  # Telegram bot webhook handler
├── handler.py              # Input sanitization, file validators, logging
├── document_loader.py      # File reading: PDF, CSV, Images (OCR)
├── requirements.txt        # Python dependencies
├── Procfile                # For Render deployment
├── .env                    # Environment variables (not committed)
├── user.db                 # SQLite log (optional)
├── templates/              # HTML templates
│   ├── ai_assistant.html
│   ├── openai_reply.html
│   ├── telegram.html
│   ├── telegram_reply.html
│   └── del_logs.html
└── static/                 # CSS/JS assets



This project was created as part of the DSAI Capstone.  
Made with ❤️ and OpenAI by Rubiyah Biamin.
