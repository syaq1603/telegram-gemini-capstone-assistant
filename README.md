# 🤖 This is a Gemini Telegram Knowledge Assistant.

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

-----------------------------------------------------------------------------------------------------

# 📚 Project Structure (Full Stack)

telegram_gemini_bot/
├── app.py                 # Flask backend entry (webhook server)
├── bot.py                 # Handles Telegram logic (text, files, replies)
├── assistant.py           # Gemini prompt generation
├── file_handler.py        # PDF/image content extraction
├── document_loader.py     # Local file (PDF, DOCX, TXT, CSV) parsing
│
├── templates/             # Frontend HTML pages for web routes
│   ├── index.html
│   ├── main.html
│   ├── gemini.html
│   ├── gemini_reply.html
│   ├── telegram.html
│   ├── logs.html
│   └── del_logs.html
│
├── static/                # (Optional) CSS, images, JS
│   └── styles.css
│
├── requirements.txt       # Dependencies
├── .env                   # Secret keys (ignored by Git)
├── .gitignore             # Keeps sensitive/unwanted files out of Git
└── README.md              # Project overview

✅ Backend (Flask):
The backend includes:

- bot.py, assistant.py → processes user inputs

- Gemini API → generates answers

- Flask → handles routing and webhooks

- file_handler.py, document_loader.py → extract text

✅ The Frontend in this project:
Two frontends:
Interface Type	Description

🟦 Telegram UI	User-facing interface (chat input/output)

🟩 Flask web interface	HTML pages served by app.py (e.g. index.html)

---------------------------------------------------------------------------------------------------------------------

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


