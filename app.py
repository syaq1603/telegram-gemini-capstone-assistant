from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Telegram bot token and public URL for the webhook from environment variables
GEMINI_TELEGRAM_TOKEN = os.getenv('GEMINI_TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # The public URL of your deployed app

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for sessions

# Ensure database exists and create a table if necessary
def init_db():
    with sqlite3.connect("user.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            );
        ''')

init_db()

# Route to the index page (Landing page)
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle user session start
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

# Route for interacting with Gemini (ask questions or upload documents)
@app.route("/gemini")
def gemini():
    return render_template("gemini.html")

# Route to handle the response from Gemini based on the user input or document upload
@app.route("/gemini_reply", methods=["POST"])
def gemini_reply():
    question = request.form.get("q")
    file = request.files.get("file")
    file_text = ""

    if file and file.filename:
        # Process the uploaded file and extract text (for PDF, CSV, or image)
        file_bytes = file.read()
        file_text = extract_text_from_file(file_bytes, file.filename)
        full_input = f"""Document:
{file_text}

User Question:
{question}"""
    else:
        full_input = question

    # Generate a response from Gemini (this can be integrated with the actual Gemini API)
    r_html = generate_financial_reply(full_input, as_html=True)
    
    return render_template("gemini_reply.html", r=r_html, file_text=file_text)

# Route to view session logs
@app.route("/logs")
def logs():
    with sqlite3.connect("user.db") as conn:
        rows = conn.execute("SELECT * FROM user ORDER BY timestamp").fetchall()
    return render_template("logs.html", r=rows)

# Route to delete all logs
@app.route("/del_logs")
def del_logs():
    with sqlite3.connect("user.db") as conn:
        conn.execute("DELETE FROM user")
    return render_template("del_logs.html")

# Route to manage Telegram bot
@app.route("/telegram_page", methods=["GET", "POST"])
def telegram_page():
    status = "The telegram bot is not running. Click the button below to start it."
    return render_template("telegram.html", status=status)

# Route to start the Telegram bot (set webhook)
@app.route("/start_telegram", methods=["GET", "POST"])
def start_telegram():
    webhook_url = f"https://api.telegram.org/bot{GEMINI_TELEGRAM_TOKEN}/setWebhook?url={WEBHOOK_URL}/telegram"
    response = requests.post(webhook_url, json={"url": WEBHOOK_URL + "/telegram"})
    
    if response.status_code == 200:
        status = "The telegram bot is running. Please check with the telegram bot."
    else:
        status = f"Failed to start the telegram bot. {response.text}"

    return render_template("telegram.html", status=status)

# Route to stop the Telegram bot (delete webhook)
@app.route("/stop_telegram", methods=["GET", "POST"])
def stop_telegram():
    webhook_url = f"https://api.telegram.org/bot{GEMINI_TELEGRAM_TOKEN}/deleteWebhook"
    response = requests.post(webhook_url)
    
    if response.status_code == 200:
        status = "The telegram bot is stopped."
    else:
        status = "Unable to stop the Telegram bot. Please check the logs."

    return render_template("telegram.html", status=status)

# Route to handle incoming Telegram webhook messages
@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()
    print(f"Received update: {update}")  # Log incoming messages (for debugging)

    # Check if the update contains a message
    if "message" in update:
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        
        # Simple logic to respond based on the message
        if text.lower() == "/start":
            reply_text = "Welcome to the Gemini Telegram Bot! How can I assist you today?"
        else:
            reply_text = f"You said: {text}"
        
        # Send a reply back to the user
        send_message_url = f"https://api.telegram.org/bot{GEMINI_TELEGRAM_TOKEN}/sendMessage"
        requests.post(send_message_url, data={"chat_id": chat_id, "text": reply_text})
    
    return "ok", 200  # Respond with "ok" to acknowledge the message

# Helper function to simulate Gemini's response generation (replace with actual API call)
def generate_financial_reply(message, as_html=False):
    # Simulating a response from the Gemini API (this can be replaced with actual logic)
    return f"AI Response to '{message}'"

# Function to extract text from the uploaded document (implement as needed)
def extract_text_from_file(file_bytes, filename):
    # Simulating text extraction from file (this should be replaced with real file parsing logic)
    return f"Extracted text from {filename}"

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5000)
