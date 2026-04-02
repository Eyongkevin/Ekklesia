import reflex as rx
from app.states.invite import InviteState

def invite_page():
    return rx.vstack(
        rx.heading("Generate Invite Link"),
        rx.button(
            "Generate Invite",
            on_click=InviteState.generate_invite
        ),
        rx.cond(
            InviteState.invite_code != "",
            rx.input(value=InviteState.invite_link, read_only=True)
        )
    )