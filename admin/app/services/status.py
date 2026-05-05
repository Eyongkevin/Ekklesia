import httpx

from app.config import settings


def get_active_status():
    response = httpx.get(f"{settings.BASE_URL}/status/")
    response.raise_for_status()
    return response.json()