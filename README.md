# 🤖 Gemini Telegram Knowledge Assistant

A Telegram bot that uses **Google Gemini** to answer user questions from uploaded documents (PDFs, DOCX). Combines Retrieval-Augmented Generation (RAG) with natural language queries.

---

# 🚀 Features

- 🧠 Gemini-powered natural language answers
- 📄 Upload PDF or DOCX files
- 🔍 Retrieves relevant info using FAISS vector search
- 💬 Chat interface via Telegram
- ☁️ Deployable to Render or Railway

---

# 🔧 Tech Stack

- Google Gemini (via `google-generativeai`)
- FAISS for similarity search
- sentence-transformers for embeddings
- python-telegram-bot for Telegram integration
- PyMuPDF and docx2txt for file parsing

---

# ⚙️ Setup Instructions

### 1. Clone the repo & install dependencies

git clone https://github.com/yourusername/gemini-telegram-assistant.git
cd gemini-telegram-assistant
pip install -r requirements.txt

# Configure .env file
Create a .env file in the root directory:
GOOGLE_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

## 🧪 Run Locally
python bot.py

## Send messages or upload documents to your bot on Telegram.

# ☁️ Deployment (Render)
1. Create requirements.txt and Procfile
Already included.

## Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/gemini-telegram-assistant.git
git push -u origin main

#3. Go to https://render.com
Create a new Web Service

Connect your GitHub repo

Set Start Command: python bot.py

Add environment variables from .env 

# 📚 Project Structure

gemini-telegram-assistant/
│
├── bot.py              # Telegram bot logic
├── assistant.py        # Gemini Q&A + FAISS search
├── document_loader.py  # Extract text from PDF/DOCX
├── .env                # API keys (not tracked)
├── requirements.txt
├── Procfile
└── README.md

## 🧠 Example Query
Upload a document
Ask: “What did the CEO say about Q2 performance?”

Gemini will respond based on your uploaded content.

# 📬 Contact
For help or feature requests, open an issue or email [syaq1603.com].


