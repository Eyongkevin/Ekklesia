from typing import Optional, TypedDict, Any
from datetime import datetime
from  app.services import users as user_services
import reflex as rx


class UserAdminType(TypedDict):
    id: str
    email: Optional[str]
    first_name: str
    last_name: Optional[str]
    is_active: bool
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

        admins = user_services.get_admin_users(
            access_token=auth_state.access_token,
            page=self.page,
            per_page=self.per_page
        )

        self.total_pages = admins.get('total', 0) // self.per_page + 1
        self.admins = admins.get('admins', [])