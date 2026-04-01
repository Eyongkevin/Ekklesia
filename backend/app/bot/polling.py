import time
import logging
import requests

from app.bot.router import route_update
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"


def get_updates(offset: int | None = None):
    """Fetch updates from Telegram API."""
    logger.info("Fetching updates from Telegram API.")

    try:
        url = f"{TELEGRAM_API}/getUpdates"
        params = {"timeout": 30, "offset": offset}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching updates: {e}")
        return None


def run_polling():
    """Start the polling loop to fetch updates from Telegram."""

    logger.info("Starting polling loop.")
    offset = None

    while True:
        data = get_updates(offset)

        if not data or 'result' not in data:
            logger.warning("No updates received or invalid response format.")
            time.sleep(1)
            continue

        for update in data["result"]:
            try:
                logger.info(f"📩 Update received: {update}")
                route_update(update)
                offset = update["update_id"] + 1
            except Exception as e:
                logger.error(f"❌ Error processing update: {e}")

        time.sleep(0.5)

if __name__ == "__main__":
    run_polling()