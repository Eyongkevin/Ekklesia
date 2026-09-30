from typing import Optional

import httpx

from app.config import settings

def get_admin_users(
        access_token: str,
        page: int=1, 
        per_page: int = 10):
    params = {
        'page': page,
        'per_page': per_page
    }
    response = httpx.get(f"{settings.BASE_URL}/users/admin/", params=params, headers={
                    "Authorization": f"Bearer {access_token}"
                })
    response.raise_for_status()
    return response.json()