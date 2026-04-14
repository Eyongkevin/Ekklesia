import httpx

BASE_URL = "http://localhost:8002/api/v1"

async def login(email: str, password: str):
    response = httpx.post(f"{BASE_URL}/users/login/", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()