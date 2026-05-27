import reflex as rx

from app.services.invite import create_invite
from app.models import invite as invite_models

class InviteState(rx.State):
    codes: list[invite_models.InviteCodeRes] = [
        invite_models.InviteCodeRes(
            id="6d589c98-f7af-40c8-8081-c9495ee2d6cf",
            expires_at= "2026-05-15T11:07:57.914945",
            expire_in="(20 days)",
            code="FBCA038-SH8EE8",
            is_active=True,
            created="2026-05-14T13:54:39.666174",
            created_by="Alex Brown",
        ),
        invite_models.InviteCodeRes(
            id="46eb549d-cb5b-4ddf-89eb-0ae713a89c21",
            expires_at= "2026-05-15T11:07:57.914945",
            expire_in="(Expired)",
            code="FBCA038-NRPZCF",
            is_active=False,
            created="2026-05-14T14:45:00.220580",
            created_by="Ayamba Derick",
        ),
        invite_models.InviteCodeRes(
            id="9b41be10-9701-4c97-8a1b-14e62353274e",
            expires_at= "",
            expire_in="Never",
            code="FBCA038-JNI50A",
            is_active=True,
            created="2026-05-16T13:04:11.303895",
            created_by="Alex Brown",
        ),
        invite_models.InviteCodeRes(
            id="f7ffa01e-1614-4a37-a02f-d1b5a9a95205",
            expires_at= "",
            expire_in= "Never",
            code="FBCA038-IN9VCL",
            is_active=False,
            created="2026-05-16T13:04:11.303895",
            created_by="Eyong Kevin",
        ),
    ]

    modal_open: bool = False
    expiry_date: str = ""          # bound to date input
    preview_suffix: str = "X7K2"  # shown in modal preview
    state: str = "All"
    status: str = "All"
    toast_message: str = ""
    toast_visible: bool = False
    copied_code: str = ""
    invite_code: str = ""
    invite_link: str = ""

    def open_modal(self):
        self.expiry_date = ""
        self.modal_open = True

    def close_modal(self):
        self.modal_open = False

    def set_expiry_date(self, value: str):
        self.expiry_date = value

    def copy_code(self, code: str):
        self.copied_code = code
        self._show_toast(f"Copied: {code}")

    def deactivate_code(self, code: str):
        # TODO: Deactivate from backend api
        self._show_toast(f"{code} deactivated.")

    def delete_code(self, code: str):
        # TODO: Delete from backend api
        self._show_toast(f"{code} deleted.")

    def _show_toast(self, msg: str):
        self.toast_message = msg
        self.toast_visible = True

    def hide_toast(self):
        self.toast_visible = False

    @rx.event
    def generate_invite(self):
        invite = create_invite(church_id="2ad0c9ae-ce92-4e21-aa09-76753fe51252")
        self.invite_code = invite["code"]
        self.invite_link = invite["link"]

    @rx.event
    def set_state(self, value: str):
        self.state = value

    @rx.event
    def set_status(self, value: str):
        self.status = value