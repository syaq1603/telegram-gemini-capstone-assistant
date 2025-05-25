import requests
import os

def set_telegram_webhook():
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/setWebhook?url={os.getenv('WEBHOOK_URL')}/telegram"
    response = requests.post(webhook_url)
    print(f"Webhook set response: {response.text}")  # Log the response for debugging
    return response

def remove_telegram_webhook():
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/deleteWebhook"
    response = requests.post(webhook_url)
    print(f"Webhook removed response: {response.text}")  # Log the response for debugging
    return response

def handle_telegram_webhook(update):
    """Handles incoming Telegram messages and sends responses."""
    try:
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']
        print(f"Received message: {user_message} from chat_id: {chat_id}")

        # Generate a response for the received message
        response = generate_telegram_reply(user_message)
        send_telegram_message(chat_id, response)
    except Exception as e:
        print(f"Error processing update: {e}")

def generate_telegram_reply(message):
    print(f"Generating response for message: {message}")
    
    # Handle basic queries
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"
    elif "inflation" in message.lower():
        return "Inflation is the rate at which the general level of prices for goods and services rises, and subsequently, the purchasing power of currency falls."
    
    # Placeholder AI response (you can replace this with actual AI integration)
    return f"You asked about: {message}"

def send_telegram_message(chat_id, text):
    telegram_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    
    # Send the message to Telegram
    response = requests.post(telegram_url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")
    else:
        print(f"Successfully sent message: {text} to chat_id: {chat_id}")
