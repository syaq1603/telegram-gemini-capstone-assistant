# app.py

from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEBHOOK_URL = "https://212f-118-200-144-21.ngrok-free.app"

# Get the Telegram bot token and ngrok URL from environment variables
gemini_telegram_token = os.getenv("GEMINI_TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # This should be your ngrok URL

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # You can keep this or use os.urandom(24) for more security

# Route to delete the webhook (Stop the bot)
@app.route("/telegram_page", methods=["GET", "POST"])
def telegram_page():
    webhook_url = f"https://api.telegram.org/bot{gemini_telegram_token}/deleteWebhook"
    response = requests.post(webhook_url, json={"url": WEBHOOK_URL, "drop_pending_updates": True})
    status = "The telegram bot is not running. Click the button below to start it."
    return render_template("telegram.html", status=status)

# Route to start the Telegram bot (Set the webhook)
@app.route("/start_telegram", methods=["GET", "POST"])
def start_telegram():
    webhook_url = f"https://api.telegram.org/bot{gemini_telegram_token}/setWebhook?url={WEBHOOK_URL}/telegram"
    
    # Set the webhook URL for the Telegram bot
    webhook_response = requests.post(webhook_url, json={"url": WEBHOOK_URL, "drop_pending_updates": True})
    
    print('Webhook response:', webhook_response)
    
    if webhook_response.status_code == 200:
        status = "The telegram bot is running. Please check with the telegram bot."
    else:
        status = "Failed to start the telegram bot. Please check the logs."
    
    return render_template("telegram.html", status=status)

# Route to stop the Telegram bot (Remove the webhook)
@app.route("/stop_telegram", methods=["GET", "POST"])
def stop_telegram():
    webhook_url = f"https://api.telegram.org/bot{gemini_telegram_token}/deleteWebhook"
    remove_webhook_response = requests.post(webhook_url)
    
    print(remove_webhook_response)
    
    if remove_webhook_response.status_code == 200:
        status = "The telegram bot is stopped."
    else:
        status = "Unable to stop telegram. Please check the logs."
    
    return render_template("telegram.html", status=status)

# Route to handle the incoming messages from Telegram
@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        if text == "/start":
            r_text = "Welcome to the Gemini Telegram Bot! You can ask me any finance-related questions."
        else:
            # You can customize the prompt here or call your model
            system_prompt = "You are a financial expert. Answer ONLY questions related to finance, economics, investing, and financial markets."
            prompt = f"{system_prompt}\n\nUser Query: {text}"

            # Replace this with the logic you want to use to generate responses
            # For example, you could use a pre-trained model here to generate `r_text`
            r_text = "This is a placeholder response for finance-related questions."  # Replace this with actual response generation logic

        # Send the response back to the user
        send_message_url = f"https://api.telegram.org/bot{gemini_telegram_token}/sendMessage"
        requests.post(send_message_url, data={"chat_id": chat_id, "text": r_text})

    return 'ok', 200

# Optional route for the payment page (If you want to add a payment feature)
@app.route("/paynow", methods=["GET", "POST"])
def paynow():
    return render_template("paynow.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)


