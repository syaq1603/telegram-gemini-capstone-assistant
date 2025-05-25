from flask import Flask, request, render_template
import os
from bot import set_telegram_webhook, remove_telegram_webhook, handle_telegram_webhook

app = Flask(__name__)

@app.route("/start_telegram", methods=["GET", "POST"])
def start_telegram():
    # Set the webhook for the Telegram bot
    set_telegram_webhook()
    status = "The Telegram bot is running. Please check with the Telegram bot."
    return render_template("telegram.html", status=status)

@app.route("/stop_telegram", methods=["GET", "POST"])
def stop_telegram():
    # Remove the webhook for the Telegram bot
    remove_telegram_webhook()
    status = "The Telegram bot is stopped."
    return render_template("telegram.html", status=status)

@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()
    print(f"Received update: {update}")  # Log the incoming update
    handle_telegram_webhook(update)
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
