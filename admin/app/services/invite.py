from datetime import datetime

import httpx

from app.config import settings
from app.utils import get_expire_at


def update_invite(access_token: str, state: str | bool, id: str | None = None, expire_date: str | None = None, expire_time: str | None = None):
    if isinstance(state, str):
        is_active: bool = True if state == 'Active' else False
    else:
        is_active = state

    expires_at = str(get_expire_at(expire_date, expire_time)) if expire_date else None

    response = httpx.patch(f"{settings.BASE_URL}/invites/{id}/", json={
                "is_active": is_active,
                "expires_at": expires_at
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
    response.raise_for_status()
    return response.json()


def create(access_token: str, code: str, state: str, expire_date: str | None, expire_time: str):
    is_active: bool = True if state == 'Active' else False
    expires_at = str(get_expire_at(expire_date, expire_time)) if expire_date else None

    response = httpx.post(f"{settings.BASE_URL}/invites/", json={
                "code": code,
                "state": is_active,
                "expires_at": expires_at
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            }
    )

    response.raise_for_status()
    return response.json()

def get_invites(
    access_token: str,
    church_id: str,
    state: str,
    is_active: str,
    page: int = 1,
    per_page: int = 10
) -> list[dict]:
    params = {
        "church_id": church_id,
        "state": None if state == "All" else state.upper(),
        "page": page,
        "per_page": per_page
    }
    evaluated_is_active: bool | None = {"All": None, "Active": True, "Inactive": False}[is_active]
    if evaluated_is_active is not None:
        params['is_active'] = evaluated_is_active

    response = httpx.get(
        f"{settings.BASE_URL}/invites/", 
        params=params,
        headers={
                "Authorization": f"Bearer {access_token}"
        }
    )
    response.raise_for_status()
    return response.json()

def delete(access_token: str, invite_id: str) -> None:
    response = httpx.delete(
        f"{settings.BASE_URL}/invites/{invite_id}/",
        headers={
                "Authorization": f"Bearer {access_token}"
        })
    response.raise_for_status()
