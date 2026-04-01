import requests

from app.bot.services.telegram import send_message


def handle_start(message: dict):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    first_name = message["from"].get("first_name", "")

    parts = text.split()
    invite_code = parts[1] if len(parts) > 1 else None

    if not invite_code:
        send_message(chat_id, "❌ Invalid invite link. Please contact your church.")
        return

    response = requests.post(
        "http://localhost:8002/api/v1/users/register",
        json={
            "telegram_id": str(chat_id),
            "first_name": first_name,
            "invite_code": invite_code
        }
    )
    if response.status_code == 200:
        user = response.json()
        send_message(
            chat_id,
            f"🎉 Welcome {user['first_name']}! You are now registered!!!"
        )
    else:
        send_message(chat_id, "❌ Registration failed. Please check your invite code and try again.")
