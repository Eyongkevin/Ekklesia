from typing import Optional

import httpx

from app.config import settings


def get_tags():
    response = httpx.get(f"{settings.BASE_URL}/announcements/tags/")
    response.raise_for_status()
    return response.json()

def submit(
    title: str,
    content: str,
    is_pinned: bool,
    links: list[dict[str, str]],
    status: str,
    created_by: str,
    church_id: str,
    publish_at: Optional[str] = None,
    expire_at: Optional[str] = None,
    tags: Optional[list[str]] = None,
    audiences: Optional[list[str]] = None
    ):

    response = httpx.post(f"{settings.BASE_URL}/announcements/", json={
        "title": title,
        "content": content,
        "is_pinned": is_pinned,
        "status": status,
        "links": links,
        "created_by": created_by,
        "church_id": church_id,
        "publish_at": publish_at,
        "expire_at": expire_at,
        "tags": tags,
        "audiences": audiences
    })
    response.raise_for_status()
    return response.json()

def get_announcements(
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
    response = httpx.get(f"{settings.BASE_URL}/announcements/", params=params)
    response.raise_for_status()
    return response.json()