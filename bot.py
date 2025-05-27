import os
import requests
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("🔐 OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")) 

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def set_telegram_webhook():
    webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={WEBHOOK_URL}/telegram"
    response = requests.post(webhook_url)
    print(f"Webhook set response: {response.text}")
    return response

def remove_telegram_webhook():
    webhook_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
    response = requests.post(webhook_url)
    print(f"Webhook removed response: {response.text}")
    return response

def is_finance_question(text):
    """Check if the message is finance-related."""
    keywords = [
        "finance", "investment", "stock", "share", "market", "inflation",
        "interest", "portfolio", "dividend", "bond", "economy", "gold",
        "cryptocurrency", "crypto", "trading", "return", "risk", "currency"
    ]
    text = text.lower()
    return any(word in text for word in keywords)

def handle_telegram_webhook(update):
    """Handles incoming Telegram messages and sends responses."""
    try:
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']

        # Log the received message and chat ID
        print("📩 Telegram webhook received!")
        print(f"🔍 Chat ID: {chat_id}")
        print(f"🗨️ Message: {user_message}")

        # Filter for finance-related topics
        if is_finance_question(user_message):
            response = generate_telegram_reply(user_message)
        else:
            response = "⚠️ I'm only able to help with questions related to finance, investing, economics, and financial markets."

        send_telegram_message(chat_id, response)

    except Exception as e:
        print(f"❌ Error processing Telegram message: {e}")

def generate_telegram_reply(message):
    """Generate a financial response using OpenAI Chat API."""
    try:
        print(f"Generating response for message: {message}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating OpenAI response: {e}")
        return "Sorry, I couldn't generate a response at the moment."

def send_telegram_message(chat_id, text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(telegram_url, data=payload)

    if response.status_code != 200:
        print(f"Error sending message: {response.text}")
    else:
        print(f"✅ Successfully sent message to chat_id {chat_id}: {text}")
