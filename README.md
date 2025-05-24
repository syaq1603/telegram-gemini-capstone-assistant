# 💼 Gemini Financial Assistant (Telegram + Web Bot)

This is a financial assistant powered by Google Gemini, accessible via both a **Telegram bot** and a **Flask web app**.

Users can:
- 📊 Ask questions about financial concepts, companies, and markets
- 📎 Upload PDFs, CSVs, or images for analysis
- 💬 Receive natural language insights powered by Gemini
- 🧾 Type `generate PDF` (via web) to export Gemini’s response
- 🔒 Chat securely with a session-based interface

---

## 🚀 How to Use

### 🖥️ On the Web
1. Open the Flask web app
2. Enter your name to start a session
3. Ask a financial question or upload a file (PDF, image, CSV)
4. View the AI-generated response and any extracted content

### 💬 On Telegram
1. Start the Telegram bot
2. Upload a file or ask a financial question
3. The bot replies with context-aware financial insights

---

## 🧱 Frontend & Backend Overview

### 🎨 Frontend (User Interface)
- **Technology**: HTML templates using Jinja2 (`templates/` folder)
- **Purpose**: Renders web forms, responses, logs, and navigation
- **Pages**:
  - `index.html`: Entry page
  - `main.html`: Main menu
  - `gemini.html`: Ask a question or upload a file
  - `gemini_reply.html`: Displays Gemini's answer
  - `logs.html`: View user logs
  - `del_logs.html`: Confirm log deletion
  - `telegram.html`: Bot status control panel

### 🧠 Backend (Server + Logic)
- **Framework**: Flask
- **APIs**:
  - Handles routes for user sessions, Gemini integration, and Telegram webhook
  - Processes uploaded files (PDF, images) and extracts text
- **LLM**: Google Gemini via `google-generativeai`
- **Database**: SQLite (`user.db`) to log session info

---

## ⚙️ Requirements

- Python 3.8+
- Telegram Bot Token
- Google Gemini API Key

### Install dependencies

```bash
pip install -r requirements.txt

```
## ▶️ Run the App Locally

python app.py

Visit: http://localhost:5000

## 📁 File Structure

telegram_gemini_capstone_assistant/
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


## Made with ❤️ using Gemini + Flask + Telegram.



