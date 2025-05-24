# bot.py
# Detect text messages
# Handle uploaded PDF or image files
# Respond using Gemini after extracting content
# bot.py

import os
import requests
from assistant import generate_financial_reply
from handler import extract_text_from_file
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("GEMINI_TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}"

def handle_telegram_webhook(update):
    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]

    # Handle text messages
    if "text" in message:
        text = message["text"].strip()
        if text.lower() == "generate pdf":
            reply = "PDF generation is available via the web interface only."
        else:
            reply = generate_financial_reply(text, as_html=False)

        send_message(chat_id, reply)

    # Handle document or photo uploads
    elif "document" in message or "photo" in message:
        file_id = (message.get("document") or message.get("photo")[-1])["file_id"]
        file_path = get_file_path(file_id)
        file_url = f"{FILE_API}/{file_path}"

        file_response = requests.get(file_url)
        content_text = extract_text_from_file(file_response.content, file_path)
        reply = generate_financial_reply(content_text, as_html=False)

        send_message(chat_id, reply)

def get_file_path(file_id):
    res = requests.get(f"{TELEGRAM_API}/getFile?file_id={file_id}")
    return res.json()["result"]["file_path"]

def send_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        data={"chat_id": chat_id, "text": text}
    )
