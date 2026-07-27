import reflex as rx

def status_icon(status: bool):
    return rx.cond(
        status,
        rx.icon("check", color="green"),
        rx.icon("x", color="red"),
    )