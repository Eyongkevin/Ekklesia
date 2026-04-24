import httpx

from app.config import settings

async def login(email: str, password: str):
    response = httpx.post(f"{settings.BASE_URL}/users/login/", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()