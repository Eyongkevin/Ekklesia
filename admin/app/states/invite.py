import reflex as rx
from app.services.invite import create_invite

class InviteState(rx.State):
    invite_code: str = ""
    invite_link: str = ""

    @rx.event
    def generate_invite(self):
        invite = create_invite(church_id="2ad0c9ae-ce92-4e21-aa09-76753fe51252")
        self.invite_code = invite["code"]
        self.invite_link = invite["link"]