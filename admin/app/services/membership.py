import httpx

BASE_URL = "http://localhost:8002/api/v1"

def get_membership_stats(church_id: str):
    response = httpx.get(f"{BASE_URL}/users/memberships/{church_id}/stats")
    response.raise_for_status()
    return response.json()