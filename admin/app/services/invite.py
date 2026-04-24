import httpx

from app.config import settings


def create_invite(church_id: str):
    response = httpx.post(f"{settings.BASE_URL}/invites/", json={"church_id": church_id})
    response.raise_for_status()
    return response.json()