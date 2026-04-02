import reflex as rx
from app.states.church import ChurchState

def church_page():
    return rx.vstack(
        rx.heading("Church Management"),

        rx.input(
            placeholder="Enter church name",
            value=ChurchState.name,
            on_change=ChurchState.set_name
        ),
        rx.button(
            "Add Church",
            on_click=ChurchState.add_church
        ),
        rx.divider(),
        rx.heading("Existing Churches"),
        rx.foreach(
            ChurchState.churches,
            lambda church: rx.text(church['name'])
        )

    )
