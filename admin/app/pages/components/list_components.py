import reflex as rx

def status_icon(status: bool):
    return rx.cond(
        status,
        rx.icon("check", color="green", size=16),
        rx.icon("x", color="red", size=16),
    )