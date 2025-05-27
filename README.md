# 📘 FINANCIAL ADVISOR CHATBOT — README

An AI-powered financial assistant that integrates **OpenAI** for intelligent financial replies and connects with users through a **Telegram bot**. Built with **Flask**, this assistant can answer questions and analyze uploaded documents, deployed on **Render**.

## 🧱 Project Structure

<pre><code>telegram_gemini_capstone_assistant/
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
</code></pre>

## 🔤 Backend: Flask API (OpenAI + Telegram)

### Key Features:

* Handles routes:

  * `/` → Ask a financial question
  * `/analyze_file` → Upload file for analysis
  * `/telegram` → Webhook endpoint for Telegram bot
  * `/start_telegram` / `/stop_telegram` → Bot control
* Uses OpenAI `gpt-3.5-turbo` for generating replies
* Logs user activity (optional)

### Key Libraries:

* `Flask`, `requests`, `openai`, `python-docx`, `PyPDF2`, `pytesseract`, `pillow`


## 🌐 Frontend: HTML + CSS (Jinja2 Templates)

### Pages:

* **`ai_assistant.html`** — Ask a question or upload a document
* **`openai_reply.html`** — Show AI response
* **`telegram.html`** — Manage Telegram bot
* **`telegram_reply.html`** — View bot start/stop results
* **`del_logs.html`** — Confirm log deletion

### UI Features:

* Simple interface for typing questions
* Document upload form
* Navigation to bot control


## 🧠 Telegram Bot Integration

* Bot username: [@tiabotbot](https://t.me/tiabotbot)
* Webhook endpoint: `/telegram`
* Accepts messages and replies using OpenAI
* Deployed and secured via Render environment

### Example:

```
User: hello
Bot: Hello! How can I assist you with finance today?
```


## 🚀 Deployment on Render

### 🔧 Setup:

1. Create a new **Web Service** on Render
2. Connect to GitHub repo
3. Add environment variables:

   ```env
   OPENAI_API_KEY=sk-...
   TELEGRAM_BOT_TOKEN=...
   WEBHOOK_URL=https://your-render-url.onrender.com
   ```
4. `Start Command:`

   ```bash
   gunicorn app:app
   ```

### 🌍 Set Telegram Webhook:

```bash
curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=<WEBHOOK_URL>/telegram"
```

## 📝 .env Template

```env
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=...
WEBHOOK_URL=https://your-render-url.onrender.com
```

> **Never commit `.env`** to GitHub.

## 🥮 Testing & Logs

* Use [Render Logs](https://dashboard.render.com) for webhook requests
* Print statements log:

  * Received messages
  * Chat IDs
  * OpenAI responses
  * Errors

## ✅ Conclusion

This project combines OpenAI, Flask, and Telegram to create a financial assistant that answers user questions and analyzes uploaded documents. It demonstrates how AI can simplify complex information and be integrated into real-time messaging platforms.

Through this work, I gained valuable experience in API integration, deployment, secure environment handling, and user interaction design. The system is modular and can be extended with features like multilingual support, user logs, and advanced file handling.


*Made with ❤️ and OpenAI by Rubiyah Biamin.*

