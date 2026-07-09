import httpx

from app.config import settings


def get_active_audience(access_token: str):
    response = httpx.get(f"{settings.BASE_URL}/audience/",
                headers={
                "Authorization": f"Bearer {access_token}"
            }
    )
    response.raise_for_status()
    return response.json()