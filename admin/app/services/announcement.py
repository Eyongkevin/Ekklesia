from typing import Optional

import httpx

from app.config import settings


def get_tags(access_token: str):
    response = httpx.get(f"{settings.BASE_URL}/announcements/tags/", headers={
            "Authorization": f"Bearer {access_token}"
    })
    response.raise_for_status()
    return response.json()

def submit(
    access_token: str,
    id: Optional[str],
    title: str,
    content: str,
    is_pinned: bool,
    links: list[dict[str, str]],
    status: str,
    church_id: str,
    publish_at: Optional[str] = None,
    expire_at: Optional[str] = None,
    tags: Optional[list[str]] = None,
    audiences: Optional[list[str]] = None
    ):

    if id:
        # Update existing announcement
        response = httpx.put(f"{settings.BASE_URL}/announcements/{id}/", json={
            "title": title,
            "content": content,
            "is_pinned": is_pinned,
            "status": status,
            "links": links,
            "church_id": church_id,
            "publish_at": publish_at,
            "expire_at": expire_at,
            "tags": tags,
            "audiences": audiences
        }, headers={"Authorization": f"Bearer {access_token}"})
    else:
        # Create new announcement
        response = httpx.post(f"{settings.BASE_URL}/announcements/", json={
            "title": title,
            "content": content,
            "is_pinned": is_pinned,
            "status": status,
            "links": links,
            "church_id": church_id,
            "publish_at": publish_at,
            "expire_at": expire_at,
            "tags": tags,
            "audiences": audiences
        }, headers={"Authorization": f"Bearer {access_token}"})
        response.raise_for_status()

    return response.json()

def delete(access_token: str, announcement_id: str) -> None:
    response = httpx.delete(f"{settings.BASE_URL}/announcements/{announcement_id}/", headers={
                "Authorization": f"Bearer {access_token}"
            })
    response.raise_for_status()

def delete_many(access_token: str, announcement_ids: list[str]) -> None:
    response = httpx.request(
        "DELETE",
        f"{settings.BASE_URL}/announcements/",
        json=announcement_ids,
        headers={
                "Authorization": f"Bearer {access_token}"
            }
    )
    response.raise_for_status()

def get_announcements(
    access_token: str,
    church_id: str,
    status: str,
    audience: str,
    tag: str,
    search: str,
    is_active: bool = True,
    page: int = 1,
    per_page: int = 10
) -> list[dict]:
    params = {
        "church_id": church_id,
        "status": status,
        "audience": audience,
        "tag": tag,
        "search": search,
        "is_active": is_active,
        "page": page,
        "per_page": per_page
    }
    response = httpx.get(f"{settings.BASE_URL}/announcements/", params=params, headers={
                "Authorization": f"Bearer {access_token}"
            })
    response.raise_for_status()
    return response.json()