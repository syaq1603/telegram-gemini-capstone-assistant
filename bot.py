from bot import set_telegram_webhook, remove_telegram_webhook, handle_telegram_webhook

@app.route("/start_telegram", methods=["GET", "POST"])
def start_telegram():
    # Set the webhook for the Telegram bot
    set_telegram_webhook()
    status = "The telegram bot is running. Please check with the telegram bot."
    return render_template("telegram.html", status=status)

@app.route("/stop_telegram", methods=["GET", "POST"])
def stop_telegram():
    # Remove the webhook for the Telegram bot
    remove_telegram_webhook()
    status = "The telegram bot is stopped."
    return render_template("telegram.html", status=status)

@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()
    handle_telegram_webhook(update)
    return "ok", 200
