import httpx

BASE_URL = "http://localhost:8002/api/v1"

def create_invite(church_id: str):
    response = httpx.post(f"{BASE_URL}/invites/", json={"church_id": church_id})
    response.raise_for_status()
    return response.json()