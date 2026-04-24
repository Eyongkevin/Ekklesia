import reflex as rx

from app.states.auth import AuthState

def dashboard_header():
    return rx.hstack(
        rx.hstack(
            rx.image(src="/logo.png", width="40px", height="40px"),
            rx.heading("Ekklesia", size="4"),
            align="center",
            spacing="2",
        ),

        rx.spacer(),

        rx.hstack(
            rx.avatar(name="User", size="3"),
            rx.button(
                "Logout",
                color_scheme="red",
                variant="soft",
                on_click=AuthState.logout
            ),
            spacing="3",
        ),

        width="100%",
        padding="1em",
        border_bottom="1px solid #eee",
        position="fixed",
        top="0",
        left="0",
        z_index="1000",
        bg="white",
    )