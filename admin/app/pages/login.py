import reflex as rx

from app.states.auth import LoginState

def login_page() -> rx.Component:
    return rx.center(
            rx.card(
            rx.vstack(
                rx.center(
                    rx.image(
                        src="https://web.reflex-assets.dev/other/logo.jpg",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Sign in to your account",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    rx.text(LoginState.error, color='red'),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Email address",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        placeholder="user@gmail.com",
                        type="email",
                        size="3",
                        width="100%",
                        value=LoginState.email,
                        on_change=LoginState.set_email,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Password", size="3", weight="medium"),
                        rx.link("Forgot password?", href="/forgot-password", size="3"),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Enter your password",
                        type="password",
                        size="3",
                        width="100%",
                        value=LoginState.password,
                        on_change=LoginState.set_password,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button("Sign in", size="3", width="100%", on_click=LoginState.login),
                spacing="6",
                width="100%",
            ),
            max_width="28em",
            size="4",
            width="100%",
        ),
        height="100vh"
    )