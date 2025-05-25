import os
import requests
import google.generativeai as genai  # For later use when integrating Gemini
from dotenv import load_dotenv
from flask import Flask, request, render_template

# Load environment variables from .env file
load_dotenv()

# Set up the Gemini API key (optional for now)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

def generate_telegram_reply(message):
    """
    Simple function to handle basic messages.
    Responds with 'Hello' if the user asks for it.
    """
    print(f"Generating response for message: {message}")

    # Respond to 'hello'
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"
    else:
        return "Sorry, I don't understand that. Ask me something about finance."

# Define route to handle incoming Telegram messages
@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()
    handle_telegram_webhook(update)
    return "ok", 200

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

# Function to send messages back to Telegram
def send_telegram_message(chat_id, text):
    telegram_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    
    # Send the message to Telegram
    response = requests.post(telegram_url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")
    else:
        print(f"Successfully sent message: {text} to chat_id: {chat_id}")

# Run the Flask app locally
if __name__ == "__main__":
    app.run(debug=True, port=5000)
