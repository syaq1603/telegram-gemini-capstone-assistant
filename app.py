# app.py

from flask import Flask, request, redirect, render_template, session, url_for
from bot import handle_telegram_webhook
import sqlite3
from datetime import datetime, timezone
import os
import requests
from handler import extract_text_from_file
from assistant import generate_financial_reply

app = Flask(__name__)
app.secret_key = "replace_this_with_a_secure_key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main", methods=["POST"])
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
    domain_url = os.getenv("WEBHOOK_URL")
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/deleteWebhook"
    requests.post(webhook_url, json={"url": domain_url, "drop_pending_updates": True})
    status = "The telegram bot is not running. Click the button below to start it."
    return render_template("telegram.html", status=status)

@app.route("/start_telegram", methods=["POST"])
def start_telegram():
    domain_url = os.getenv("WEBHOOK_URL")
    webhook_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/setWebhook?url={domain_url}/telegram"
    response = requests.post(webhook_url, json={"url": domain_url, "drop_pending_updates": True})
    status = "The telegram bot is running. Please check with the telegram bot." if response.status_code == 200 else "Failed to start the telegram bot."
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
    update = request.get_json()
    handle_telegram_webhook(update)
    return "ok", 200

if __name__ == "__main__":
    print("✅ Flask is starting...")
    app.run(debug=True, port=5000)


