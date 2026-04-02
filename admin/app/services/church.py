import httpx

BASE_URL = "http://localhost:8002/api/v1"

def create_church(name: str):
    response = httpx.post(f"{BASE_URL}/churches/", json={"name": name})
    response.raise_for_status()
    return response.json()

def get_churches():
    response = httpx.get(f"{BASE_URL}/churches/")
    response.raise_for_status()
    return response.json()