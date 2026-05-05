import httpx

from app.config import settings


def get_active_audience():
    response = httpx.get(f"{settings.BASE_URL}/audience/")
    response.raise_for_status()
    return response.json()