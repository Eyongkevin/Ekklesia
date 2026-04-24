import httpx

from app.config import settings

def get_membership_stats(church_id: str):
    response = httpx.get(f"{settings.BASE_URL}/users/memberships/{church_id}/stats")
    response.raise_for_status()
    return response.json()