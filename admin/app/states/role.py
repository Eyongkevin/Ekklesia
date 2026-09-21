from typing import Optional, TypedDict, List
from datetime import date, datetime
import reflex as rx

from app.states import permission as permission_states
from app.services import role as role_services

class RoleType(TypedDict):
    id: str
    system_role_id: Optional[str]
    name: str
    description: Optional[str]
    is_active: bool
    is_protected: bool
    template_version: Optional[int]
    is_customized: bool
    created_at: datetime
    modified_at: datetime
    permissions: list[dict[str, str | bool | None]]


class RoleState(rx.State):
    show_add_update_drawer: bool = False

    @rx.var
    def get_template_versions(self) -> list[str]:
        return ["All"] + [
            str(version)
            for version in role_services.get_template_versions()
        ]

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
    from_system: str = "All"
    version: str = "All"
    active: str = "All"
    customized: str = "All"

    async def set_search(self, value: str):
        self.search = value
        role_list_state = await self.get_state(RoleListState)
        await role_list_state.paginated_roles()

    async def set_from_system(self, value: str):
        self.from_system = value
        role_list_state = await self.get_state(RoleListState)
        await role_list_state.paginated_roles()

    async def set_version(self, value: str):
        self.version = value
        role_list_state = await self.get_state(RoleListState)
        await role_list_state.paginated_roles()

    async def set_active(self, value: str):
        self.active = value
        role_list_state = await self.get_state(RoleListState)
        await role_list_state.paginated_roles()

    async def set_customized(self, value: str):
        self.customized = value
        role_list_state = await self.get_state(RoleListState)
        await role_list_state.paginated_roles()

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
                id=self.id,
                name=self.name,
                description = self.description,
                permissions = self.selected_permissions
            )
            if self.id:
                yield rx.toast.success("Role updated")
            else:
                yield rx.toast.success("Role created")

            role_list_state = await self.get_state(RoleListState)
            await role_list_state.paginated_roles()
            self.reset_form()
            
        except Exception as ex:
            yield rx.toast.error(f"Error submitting role")

class RoleListState(rx.State):
    roles: list[RoleType] = []

    page: int = 1
    per_page: int = 10
    total_pages: int = 1

    selected_ids: dict[str, str] = dict()
    roles_to_be_deleted: list[RoleType]
    users_first_name: list[str]
    show_before_deletion_modal: bool = False

    open_menu_id: int | None = None

    show_view_modal: bool = False
    selected_role: Optional[RoleType] = None
    actions_value: str = ""
    show_deletion_modal: bool = False

    all_role_names: list[dict[str, str]]
    role_name_to_be_replaced_with: str


    @rx.event
    def open_deletion_modal(self):
        self.show_deletion_modal = True
        self.show_view_modal = False

    @rx.event
    def close_deletion_modal(self):
        self.roles_to_be_deleted = []
        self.show_deletion_modal = False

    @rx.event
    def open_view_modal(self, role: RoleType):
        self.selected_role = role
        self.show_view_modal = True

    @rx.event
    def close_view_modal(self):
        self.selected_role = None
        self.show_view_modal = False

    @rx.event
    def open_before_deletion_modal(self, users_first_name: list[str]):
        self.users_first_name = users_first_name
        self.show_before_deletion_modal = True

    @rx.event
    def close_before_deletion_modal(self):
        self.role_name_to_be_replaced_with = ""
        self.show_before_deletion_modal = False

    @rx.event
    def set_role_name_to_be_replaced_with(self, value: str) -> None:
        self.role_name_to_be_replaced_with = value

    @rx.var
    def role_name_to_be_replaced_with_is_not_set(self) -> bool:
        return len(self.role_name_to_be_replaced_with) == 0

    async def paginated_roles(self) -> None:
        from app.states.auth import AuthState

        auth_state = await self.get_state(AuthState)
        filter_state = await self.get_state(RoleFilterState)

        roles = role_services.get_roles(
            access_token=auth_state.access_token,
            search=filter_state.search,
            from_system=filter_state.from_system,
            version=filter_state.version,
            customized=filter_state.customized,
            active=filter_state.active,
            page=self.page,
            per_page=self.per_page
        )

        self.total_pages = roles.get('total', 0) // self.per_page + 1
        self.roles = roles.get('roles', [])

    @rx.event
    async def update_role(self, role: RoleType):
        if role['is_protected']:
            return

        form_state = await self.get_state(RoleFormState)
        form_state.id = role['id']
        form_state.name = role['name']
        form_state.description = role['description']
        form_state.selected_permissions = [permission['name'] for permission in role['permissions']]

        self.show_view_modal = False

        role_state = await self.get_state(RoleState)
        await role_state.open_add_update_drawer()

    @rx.event
    async def get_all_roles(self, excluded_role_name:str):
        from app.states.auth import AuthState
        
        auth_state = await self.get_state(AuthState)

        all_role_names = role_services.get_all_roles(access_token=auth_state.access_token)
        self.all_role_names = [role  for role in all_role_names if role['name'] != excluded_role_name]

    @rx.var
    def get_all_role_names(self) -> list[str]:
        return [role["name"] for role in self.all_role_names]

    @rx.event
    async def delete(self, role: RoleType):
        from app.states.auth import AuthState
        
        auth_state = await self.get_state(AuthState)
        role_memberships = role_services.get_role_with_membership(auth_state.access_token, role['id'])
        self.roles_to_be_deleted = [role]

        if role_memberships['memberships']:
            await self.get_all_roles(role["name"])
            users_first_name = [membership['user']['first_name'] for membership in role_memberships['memberships']]
            self.open_before_deletion_modal(users_first_name)
        else:
            self.open_deletion_modal()

    @rx.event
    async def delete_on_confirmation(self):
        from app.states.auth import AuthState

        auth_state = await self.get_state(AuthState)

        try:
            if len(self.roles_to_be_deleted) == 1:
                role_services.delete_role(auth_state.access_token, self.roles_to_be_deleted[0]['id'])

                yield rx.toast.success("Role deleted successfully")

                self.close_deletion_modal()

                role_list_state = await self.get_state(RoleListState)
                await role_list_state.paginated_roles()
            else:
                raise NotImplementedError("Multiple Roles can't be deleted for now")
        except Exception as ex:
            yield rx.toast.error("Error deleting role")
            # error = ex.response.json()
            # yield rx.toast.error(error.get("detail", "Error deleting role"))

    @rx.event
    async def update_role_state(self, role: RoleType):
        from app.states.auth import AuthState
        auth_state = await self.get_state(AuthState)

        try:
            role_services.update_state(
                access_token=auth_state.access_token,
                role_id=role["id"],
                state= not role["is_active"],
            )
            role_list_state = await self.get_state(RoleListState)
            await role_list_state.paginated_roles()
        except Exception as ex:
            yield rx.toast.error(f"Error updating role state: {ex}")


    # @rx.event
    # async def merge_role(self):
    #     from app.states.auth import AuthState
                
    #     auth_state = await self.get_state(AuthState)
    #     role_services.merge_role(auth_state.access_token, self.role_to_be_deleted.get('id'), self.role_name_to_be_replaced_with)

    #     self.close_before_deletion_modal()
