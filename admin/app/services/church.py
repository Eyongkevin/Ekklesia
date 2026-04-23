from typing import Optional

import httpx

BASE_URL = "http://localhost:8002/api/v1"

def create_church(name: str):
    response = httpx.post(f"{BASE_URL}/churches/", json={
        "name": name
    })
    response.raise_for_status()
    return response.json()

def get_churches():
    response = httpx.get(f"{BASE_URL}/churches/")
    response.raise_for_status()
    return response.json()

def get_church_by_user(user_id: str):
    response = httpx.get(f"{BASE_URL}/churches/user/{user_id}")
    response.raise_for_status()
    return response.json()

# CONTACT

def create_church_contact(
    church_id: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    address_line: Optional[str] = None,
    phone_1: Optional[str] = None,
    phone_2: Optional[str] = None,
    email: Optional[str] = None,
    facebook: Optional[str] = None,
    youtube: Optional[str] = None,
    instagram: Optional[str] = None,
    website: Optional[str] = None) -> dict[str, str]:

    response = httpx.post(f"{BASE_URL}/churches/contact/", json={
        "church_id": church_id,
        "country": country,
        "city": city,
        "address_line": address_line,
        "phone_1": phone_1,
        "phone_2": phone_2,
        "email": email,
        "facebook": facebook,
        "youtube": youtube,
        "instagram": instagram,
        "website": website

    })
    response.raise_for_status()
    return response.json()

def get_church_contact(church_id: str):
    response = httpx.get(f"{BASE_URL}/churches/contact/{church_id}")
    response.raise_for_status()
    return response.json()

# THEME
def create_or_update_church_theme(
        church_id: str,
        year: int,
        theme: str,
        verse: str
):
    response = httpx.post(f"{BASE_URL}/churches/theme/", json={
        "church_id": church_id,
        "year": year,
        "theme": theme,
        "verse": verse
    })
    response.raise_for_status()
    return response.json()

def get_church_them_by_year(church_id: str, year: int):
    response = httpx.get(f"{BASE_URL}/churches/theme/{church_id}/{year}")
    response.raise_for_status()
    return response.json()