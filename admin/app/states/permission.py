from typing import Optional, TypedDict, List

import reflex as rx

from app.services import permission as permission_services

def format_permissions(permissions: list[dict[str, str | bool | None]]) -> dict[str, list[str]] :
    permission_group: dict[str, list[str]] = {}
    for permission in permissions:
        key = f"{permission['code'].split(':')[0].title()} Management"
        if key in permission_group:
            permission_group[key].append(permission['name'])
        else:
            permission_group[key] = [permission['name']]

    return permission_group
    

class PermissionState(rx.State):
    permissions_group: dict[str, list[str]]
    show_add_update_drawer: bool = False

    def fetch_permissions(self, access_token: str) -> None:
        self.permissions_group = format_permissions(permission_services.get_permissions(access_token))