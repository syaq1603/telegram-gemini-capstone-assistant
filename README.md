# 🤖 This is a Gemini Telegram Knowledge Assistant.

# 🤖 Telegram Gemini Capstone Bot

This is a **Telegram bot powered by Google Gemini** designed to help users with their **financial queries**. It integrates conversational AI with document analysis and PDF generation to create a smart and interactive financial assistant.

---

## ✨ Features

- 🧠 **Answer financial questions** — from basic terms to deeper insights
- 📄 **Analyze uploaded PDFs and CSVs** — such as reports, tables, or statements
- 🖼️ **Understand image-based content** (charts, graphs, screenshots)
- 📥 **Generate a PDF** of the bot's latest response by typing:  


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

# 📚 Project Structure

telegram-gemini-bot/
│
├── main.py                # Webhook + bot setup
├── handlers.py            # Message/file handlers
├── assistant.py           # Gemini logic
├── document_loader.py     # Extracts text from PDF/CSV/image
├── pdf_generator.py       # Creates a PDF from bot responses
├── image_generator.py     # (Optional) Gemini image generation
├── requirements.txt
├── .env
└── README.md

## Step-by-Step Implementation Plan

- main.py: Flask-based webhook server for Telegram

- handlers.py: Handles messages, file uploads, and /generate_pdf

- assistant.py: Sends queries to Gemini and returns response

- pdf_generator.py: Converts text replies to a downloadable PDF

- image_generator.py (optional): Uses a model or fallback method

- Webhook-ready deployment (Render or Railway)

## 🧠 Example Query
Upload a document
Ask: “What did the CEO say about Q2 performance?”

Gemini will respond based on your uploaded content.

# 📬 Contact
For help or feature requests, open an issue or email [syaq1603.com].


