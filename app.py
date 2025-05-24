# app.py

from flask import Flask, request, redirect, render_template, session, url_for
import sqlite3
from datetime import datetime, timezone
import os
import requests

# Set the correct public URL for ngrok
WEBHOOK_URL = "https://c4c1-118-200-144-21.ngrok-free.app"  # Use your ngrok URL here

from dotenv import load_dotenv
load_dotenv()

# Access the new token
bot_token = os.getenv("GEMINI_TELEGRAM_TOKEN")

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)


# Ensure this environment variable is set correctly with the public URL of your app
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    name = request.form.get("name")
    if not name:
        return redirect(url_for("index"))
    session["name"] = name
    t = datetime.now(timezone.utc)
    with sqlite3.connect("user.db") as conn:
        conn.execute("INSERT INTO user (name, timestamp) VALUES (?, ?)", (name, t))
    return render_template("main.html")

@app.route("/gemini")
def gemini():
    return render_template("gemini.html")

@app.route("/gemini_reply", methods=["POST"])
def gemini_reply():
    question = request.form.get("q")
    file = request.files.get("file")
    file_text = ""

    if file and file.filename:
        file_bytes = file.read()
        file_text = extract_text_from_file(file_bytes, file.filename)
        full_input = f"""Document:
{file_text}

User Question:
{question}"""
    else:
        full_input = question

    r_html = generate_financial_reply(full_input, as_html=True)
    return render_template("gemini_reply.html", r=r_html, file_text=file_text)

@app.route("/logs")
def logs():
    with sqlite3.connect("user.db") as conn:
        rows = conn.execute("SELECT * FROM user ORDER BY timestamp").fetchall()
    log_text = "\n".join(str(row) for row in rows)
    return render_template("logs.html", r=log_text)

@app.route("/del_logs")
def del_logs():
    with sqlite3.connect("user.db") as conn:
        conn.execute("DELETE FROM user")
    return render_template("del_logs.html")

@app.route("/telegram_page", methods=["GET", "POST"])
def telegram_page():
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/deleteWebhook"
    response = requests.post(webhook_url, json={"url": WEBHOOK_URL, "drop_pending_updates": True})
    status = "The telegram bot is not running. Click the button below to start it."
    return render_template("telegram.html", status=status)

@app.route("/start_telegram", methods=["GET", "POST"])
def start_telegram():
    # Check if the webhook is already set
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/setWebhook?url={WEBHOOK_URL}/telegram"
    
    # Print the webhook URL for debugging
    print("Setting webhook to:", webhook_url)
    
    # Only set the webhook once (check the response from Telegram)
    response = requests.post(webhook_url, json={"url": WEBHOOK_URL, "drop_pending_updates": True})
    
    # Print the response from Telegram for debugging
    print(f"Telegram response status: {response.status_code}")
    print(f"Telegram response content: {response.text}")
    
    if response.status_code == 200:
        status = "The telegram bot is running. Please check with the telegram bot."
    else:
        status = f"Failed to start the telegram bot. {response.text}"
    
    return render_template("telegram.html", status=status)


@app.route("/stop_telegram", methods=["POST"])
def stop_telegram():
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/deleteWebhook"
    response = requests.post(webhook_url)
    status = "The telegram bot is stopped." if response.status_code == 200 else "Unable to stop Telegram."
    return render_template("telegram.html", status=status)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/telegram", methods=["POST"])
def telegram():
    try:
        # Get the incoming update from Telegram
        update = request.get_json()

        # Log the incoming update for debugging purposes
        print(f"Received update: {update}")

        # Process the update (for example, handle the message)
        handle_telegram_webhook(update)

        # Return a 200 OK response to Telegram
        return "ok", 200

    except Exception as e:
        # Log any errors that occur while processing the update
        print(f"Error processing update: {e}")

        # Return a 500 error to Telegram if something goes wrong
        return "Error", 500


def handle_telegram_webhook(update):
    """Handles incoming Telegram messages and sends responses."""
    try:
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']
        print(f"Received message: {user_message} from chat_id: {chat_id}")

        # Generate a response for the received message
        response = generate_telegram_reply(user_message)
        
        # Send the response back to the user
        send_telegram_message(chat_id, response)
    except Exception as e:
        print(f"Error processing update: {e}")

def generate_telegram_reply(message):
    print(f"Generating response for message: {message}")
    
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"
    else:
        return f"You said: {message}"

def send_telegram_message(chat_id, text):
    telegram_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    
    # Send the message to Telegram
    response = requests.post(telegram_url, data=payload)

    if response.status_code != 200:
        print(f"Error sending message: {response.text}")
    else:
        print(f"Successfully sent message: {text} to chat_id: {chat_id}")

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5000)

