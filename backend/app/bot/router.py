from app.bot.handlers.start import handle_start


def route_update(update: dict):
    message = update.get("message")

    if not message:
        return

    text = message.get("text", "")

    if text.startswith("/start"):
        handle_start(message)