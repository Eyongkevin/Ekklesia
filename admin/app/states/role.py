from typing import Optional, TypedDict, List
from datetime import date
import reflex as rx

from app.states import permission as permission_states
from app.services import role as role_services


class RoleState(rx.State):
    show_add_update_drawer: bool = False

    @rx.event
    async def open_add_update_drawer(self):
        from app.states.auth import AuthState

        auth_state = await self.get_state(AuthState)

        permission_state = await self.get_state(permission_states.PermissionState)
        permission_state.fetch_permissions(auth_state.access_token)
        self.show_add_update_drawer = True

    @rx.event
    async def close_add_update_drawer(self):
        self.show_add_update_drawer = False
        
        role_form_state = await self.get_state(RoleFormState)
        role_form_state.reset_form()

class RoleFilterState(rx.State):
    search: str = ""

    async def set_search(self, value: str):
        self.search = value

class RoleFormState(rx.State):
    id: str = ""
    name: str
    max_name_len: int = 50
    description: Optional[str] = None
    selected_permissions: list[str]

    @rx.event
    def set_name(self, value: str) -> None:
        self.name = value
    
    @rx.event
    def set_description(self, value: str) -> None:
        self.description = value

    @rx.event
    def reset_form(self):
        self.reset()
        self.description = ""

    @rx.var
    def get_name_len(self) -> int:
        return len(self.name)
    
    @rx.var
    def toggle_submit_disable(self) -> bool:
        return not (len(self.name) > 0 and len(self.selected_permissions) > 0)
    
    def toggle_permission_select(self, permission_name: str):
        if permission_name in self.selected_permissions:
            self.selected_permissions.remove(permission_name)
        else:
            self.selected_permissions.append(permission_name)

    async def submit(self):
        from app.states.auth import AuthState

        auth_state: AuthState = await self.get_state(AuthState)

        try:
            role_services.create(
                access_token= auth_state.access_token,
                name=self.name,
                description = self.description,
                permissions = self.selected_permissions
            )
            self.reset_form()
            yield rx.toast.success("Role created")
        except Exception as ex:
            yield rx.toast.error(f"Error submitting role")