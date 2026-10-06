from typing import Optional, TypedDict, Any
from datetime import datetime
from  app.services import users as user_services
import reflex as rx

from app.utils import format_created_by


class UserAdminType(TypedDict):
    id: str
    email: Optional[str]
    first_name: str
    last_name: Optional[str]
    is_active: bool
    created_by: Optional["UserAdminType"]
    created_by_name: str
    memberships: list[dict[str, list[dict[str, str]]]]
    created_at: datetime
    modified_at: datetime

class UserAdminListState(rx.State):
    admins: list[UserAdminType] = []

    page: int = 1
    per_page: int = 10
    total_pages: int = 1

    async def paginated_admins(self) -> None:
        from app.states.auth import AuthState

        auth_state = await self.get_state(AuthState)
        filter_state = await self.get_state(UserAdminFilterState)

        admins = user_services.get_admin_users(
            access_token=auth_state.access_token,
            search=filter_state.search,
            is_active=filter_state.is_active,
            role=filter_state.role,
            page=self.page,
            per_page=self.per_page
        )

        self.total_pages = admins.get('total', 0) // self.per_page + 1
        self.admins = [
            {
                **admin,
                "created_by_name": format_created_by(admin.get("created_by"))

            }
            for admin in admins.get('admins', [])
        ]

class UserAdminFilterState(rx.State):
    search: str = ""
    is_active: str = "All"
    role: str = "All"

    async def set_search(self, value: str):
        self.search = value
        admin_list_state = await self.get_state(UserAdminListState)
        await admin_list_state.paginated_admins()

    async def set_is_active(self, value: str):
        self.is_active = value
        admin_list_state = await self.get_state(UserAdminListState)
        await admin_list_state.paginated_admins()

    async def set_role(self, value: str):
        self.role = value
        admin_list_state = await self.get_state(UserAdminListState)
        await admin_list_state.paginated_admins()