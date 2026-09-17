from typing import Optional

import httpx

from app.config import settings


def create(
        access_token: str, 
        id: Optional[str],
        name: str, 
        permissions: list[str],
        system_role_id: Optional[str] = None,
        template_version: Optional[int] = None,
        is_customized: Optional[bool] = False,
        description: Optional[str]=None,
        is_active: bool=True
    ):
    if id:
        response = httpx.patch(f"{settings.BASE_URL}/roles/{id}/", json={
                        "name": name,
                        "description": description,
                        "permissions": permissions
                    },
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    }
            )
    else:
        response = httpx.post(f"{settings.BASE_URL}/roles/", json={
                    "name": name,
                    "system_role_id": system_role_id,
                    "template_version": template_version,
                    "is_customized": is_customized,
                    "description": description,
                    "is_active": is_active,
                    "permissions": permissions
                },
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
        )

    response.raise_for_status()
    return response.json()

def get_roles(access_token: str, search: str, page: int=1, per_page: int = 10) -> list[dict]:
    params = {
        'search': search,
        'page': page,
        'per_page': per_page
    }
    response = httpx.get(f"{settings.BASE_URL}/roles/", params=params, headers={
                    "Authorization": f"Bearer {access_token}"
                })
    response.raise_for_status()
    return response.json()

def get_all_roles(access_token: str) -> list[dict]:
    response = httpx.get(f"{settings.BASE_URL}/roles/all/", headers={
                    "Authorization": f"Bearer {access_token}"
                })
    response.raise_for_status()
    return response.json()

def get_role_with_membership(access_token: str, role_id: str):
    response = httpx.get(f"{settings.BASE_URL}/roles/{role_id}/", headers={
            "Authorization": f"Bearer {access_token}"
    })
    response.raise_for_status()
    return response.json()

def merge_role(access_token: str, source_role_id: str, target_role_name: str):
    response = httpx.post(f"{settings.BASE_URL}/roles/{source_role_id}/merge/", json={
            "target_role_name": target_role_name,
        },
        headers={
                "Authorization": f"Bearer {access_token}"
        })
    response.raise_for_status()
    return response.json()

def delete_role(access_token: str, role_id: str) -> None:
    response = httpx.delete(f"{settings.BASE_URL}/roles/{role_id}/", headers={
                    "Authorization": f"Bearer {access_token}"
                })
    response.raise_for_status()