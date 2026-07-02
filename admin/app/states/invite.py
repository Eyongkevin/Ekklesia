from typing import Optional, TypedDict

from datetime import datetime
import string
import random

import reflex as rx

from app.services import invite as invite_service
from app.models import invite as invite_models
from app.utils import get_expire_at
from app.states.church import ChurchState

from app.config import settings



class InviteType(TypedDict):
    id: str
    expires_at: Optional[str]
    code: str
    church_id: str
    expire_in: Optional[str]
    creator: dict[str, str]
    is_active: bool
    created_at: str
    modified_at: str

class InviteState(rx.State):
    show_add_update_drawer: bool = False
    modal_open: bool = False
    expiry_date: str = ""          # bound to date input
    state: str = "All"
    status: str = "All"
    toast_message: str = ""
    toast_visible: bool = False
    copied_code: str = ""
    invite_code: str = ""
    invite_link: str = ""

    @rx.event
    async def open_add_update_drawer(self):
        invite_form_state: InviteFormState = await self.get_state(InviteFormState)
        invite_form_state.reset_form()

        self.show_add_update_drawer = True

    @rx.event
    async def close_add_update_drawer(self):
        self.show_add_update_drawer = False
        form_state = await self.get_state(InviteFormState)
        form_state.reset_form()

    def open_modal(self):
        self.expiry_date = ""
        self.modal_open = True

    def close_modal(self):
        self.modal_open = False

class InviteFormState(rx.State):
    id: str = ""
    state: str = "Active"
    code: str = ""
    church_code: str = ""
    expire_date: Optional[str] = None
    is_expire_date_lesser_than_today_date: bool = False
    expire_time: str = ""
    is_expire_time_lesser_than_today_time: bool = False
    is_time_set_but_date_not_set: bool = False
    toggle_disable_expire_time: bool = True

    @rx.event
    def set_state(self, value: str):
        self.state = value

    @rx.event
    def set_expire_date(self, value: str):
        self.expire_date = value

        if self.expire_date:
            self.is_expire_date_lesser_than_today_date = (
                self.expire_date < str(datetime.now().date())
            )
            self.verify_expire_time()
        else:
            self.is_expire_date_lesser_than_today_date = False
        self.set_toggle_disable_expire_time()

    @rx.event
    def set_expire_time(self, value: str):
        self.expire_time = value
        self.verify_expire_time()

    def verify_expire_time(self):
        if self.expire_time != "":
            try:
                self.is_expire_time_lesser_than_today_time = (
                    str(get_expire_at(self.expire_date, self.expire_time)) < datetime.now().strftime("%Y-%m-%d %H:%M")
                )
                self.is_time_set_but_date_not_set = False
            except Exception:
                self.is_time_set_but_date_not_set = True
        else:
            self.is_expire_time_lesser_than_today_time = False
            self.is_time_set_but_date_not_set = False

    @rx.event
    def reset_form(self):
        self.id = ""
        self.state = "Active"
        self.generate_code()
        self.expire_time = ""
        self.expire_date = None

        self.is_expire_time_lesser_than_today_time = False
        self.is_expire_date_lesser_than_today_date = False
        self.toggle_disable_expire_time = True


    @rx.event
    def generate_code(self)-> None:
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


    def set_toggle_disable_expire_time(self):
        self.toggle_disable_expire_time =  not self.expire_date  or  self.is_expire_date_lesser_than_today_date
        if not self.expire_date:
            self.expire_time = ""

    async def update(self):
        from app.states.auth import AuthState

        auth_state = await self.get_state(AuthState)
        try:
            updated_invite = invite_service.update_invite(
                access_token=auth_state.access_token,
                id=self.id,
                state=self.state,
                expire_date=self.expire_date,
                expire_time=self.expire_time if self.expire_time != "" else "23:59"
            )

            invite_list_state = await self.get_state(InvitetListState)
            invite_filter_state = await self.get_state(InviteFilterState)

            if invite_filter_state.is_active == "All" and invite_filter_state.state == "All":
                for i, invite in enumerate(invite_list_state.invites):
                    if invite['id'] == updated_invite['id']:
                        invite_list_state.invites[i] = updated_invite
                        break
            else:
                await invite_list_state.paginated_invites()
            yield rx.toast.success("Invite state updated")

        except Exception as ex:
            yield rx.toast.error(f"Error updating invite state: {ex}")

    async def create(self):
        from app.states.auth import AuthState
        
        auth_state = await self.get_state(AuthState)
        try:
            invite_service.create(
                auth_state.access_token,
                self.code,
                self.state,
                self.expire_date,
                self.expire_time if self.expire_time != "" else "23:59"
            )

            invite_list_state = await self.get_state(InvitetListState)

            await invite_list_state.paginated_invites()
            yield rx.toast.success("Invite code created")
            self.reset_form()
            
        except Exception as ex:
            yield rx.toast.error(f"Error creating invite code: {ex}")

class InviteFilterState(rx.State):
    is_active: str = "All"
    state: str = "All"

    @rx.event
    async def set_is_active(self, value: str):
        self.is_active = value
        invite_list_state = await self.get_state(InvitetListState)
        await invite_list_state.paginated_invites()

    @rx.event
    async def set_state(self, value: str):
        self.state = value
        invite_list_state = await self.get_state(InvitetListState)
        await invite_list_state.paginated_invites()

class InvitetListState(rx.State):
    invites: list[InviteType] = []

    page: int = 1
    per_page: int = 10
    total_pages: int = 1

    selected_ids: set[str] = set()

    open_menu_id: int | None = None

    show_view_modal: bool = False
    selected_invite: Optional[InviteType] = None

    @rx.event
    def copy_code(self, code: str):
        shared_link = f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={code}"
        yield rx.set_clipboard(shared_link)
        yield rx.toast.success(f"Copied: {code}")
    
    @rx.event
    async def update_invite_state(self, invite: InviteType):
        from app.states.auth import AuthState

        expires_at: datetime | None = datetime.fromisoformat(invite['expires_at']) if invite['expires_at'] else None
        expire_date: str | None = str(expires_at.date()) if expires_at else None
        expire_time: str = expires_at.strftime('%H:%M') if expires_at else ""

        auth_state = await self.get_state(AuthState)
        try:
            updated_invite = invite_service.update_invite(
                access_token=auth_state.access_token,
                id=invite["id"],
                state= not invite["is_active"],
                expire_date= expire_date,
                expire_time=expire_time
            )

            invite_list_state = await self.get_state(InvitetListState)
            invite_filter_state = await self.get_state(InviteFilterState)

            if invite_filter_state.is_active == "All" and invite_filter_state.state == "All":
                for i, invite in enumerate(self.invites):
                    if invite['id'] == updated_invite['id']:
                        self.invites[i] = updated_invite
                        break
            else:
                await invite_list_state.paginated_invites()
            
            yield rx.toast.success("Invite state updated")

        except Exception as ex:
            yield rx.toast.error(f"Error updating invite state: {ex}")


    @rx.event
    async def prefil_form_for_update(self, invite: InviteType):
        expire_date: datetime | None = datetime.fromisoformat(invite["expires_at"]) if invite["expires_at"] else None

        form_state = await self.get_state(InviteFormState)
        form_state.id = invite["id"]
        form_state.state = "Active" if invite["is_active"] else "Inactive"
        form_state.set_expire_date(str(expire_date.date()) if expire_date else "")
        form_state.set_expire_time(f"{expire_date.strftime('%H:%M')}" if expire_date else "")
        form_state.code = invite["code"].split("-")[1]


        invite_state = await self.get_state(InviteState)

        self.show_view_modal = False
        invite_state.show_add_update_drawer = True

    @rx.event
    async def delete(self, invite_id: str):
        from app.states.auth import AuthState

        auth_state = await self.get_state(AuthState)
        invite_service.delete(auth_state.access_token, invite_id)

        for i, invite in enumerate(self.invites):
            if invite['id'] == invite_id:
                del self.invites[i]
                break
        yield rx.toast.success("Invite deleted")

    async def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            await self.paginated_invites()

    async def prev_page(self):
        if self.page > 1:
            self.page -= 1
            await self.paginated_invites()

    async def paginated_invites(self)-> None:
        from app.states.auth import AuthState
        
        auth_state = await self.get_state(AuthState)
        church_state: ChurchState = await self.get_state(ChurchState)
        church_id = church_state.church.get('id')

        filter_state = await self.get_state(InviteFilterState)

        invites = invite_service.get_invites(
            auth_state.access_token,
            church_id=church_id,
            state=filter_state.state,
            is_active=filter_state.is_active,
            page=self.page,
            per_page=self.per_page
        )
        self.total_pages = invites.get("total", 0) // self.per_page + 1
        self.invites = invites.get("invites", [])
