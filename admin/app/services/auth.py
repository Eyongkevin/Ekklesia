import httpx

from app.config import settings

async def login(email: str, password: str):
    response = httpx.post(
        f"{settings.BASE_URL}/users/login/",
        data={
            "grant_type": "password",
            "username": email,
            "password": password,
        },
    )
    response.raise_for_status()
    return response.json()