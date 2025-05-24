from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from assistant import add_document, rag_ask
from document_loader import extract_text
from dotenv import load_dotenv
import os
import tempfile

# Load tokens
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# In-memory user doc state (per session)
user_uploaded = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Upload a PDF or DOCX file, then ask your question.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle uploaded documents (PDF/DOCX)"""
    file = await update.message.document.get_file()
    filename = update.message.document.file_name

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{filename.split('.')[-1]}") as tmp:
        await file.download_to_drive(tmp.name)
        try:
            text = extract_text(tmp.name)
            add_document(text)
            user_uploaded[update.message.from_user.id] = True
            await update.message.reply_text("✅ Document received and processed. You can now ask questions!")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user questions after upload"""
    uid = update.message.from_user.id
    if not user_uploaded.get(uid):
        await update.message.reply_text("❗Please upload a PDF or DOCX file first.")
        return

    question = update.message.text
    try:
        response = rag_ask(question)
        await update.message.reply_text(response)
    except Exception as e:
        await update.
