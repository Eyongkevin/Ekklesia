"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from app.pages.church import church_page
from app.pages.invite import invite_page
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.states.auth import AuthState

from rxconfig import config


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()

app.add_page(index)
app.add_page(church_page, route="/churches", title="Church Management")
app.add_page(invite_page, route="/invites", title="Invite Management")
app.add_page(login_page, route="/login", title="Ekklesia Login")
app.add_page(dashboard_page, route='/dashboard', on_load=AuthState.check_auth, title='Ekklesia Dashboard')
