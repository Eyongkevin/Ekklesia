import reflex as rx

from app.states.role import RoleListState


def delete_confirmation_modal():
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.icon("triangle-alert", size=30, color="red"),
                rx.heading("Please Confirm", size="4"),
                rx.dialog.description(
                    "The following Role(s) would be deleted."
                ),
                align="center"
            ),
            rx.inset(
                rx.list.unordered(
                        rx.foreach(
                            RoleListState.roles_to_be_deleted,
                            lambda role: rx.list.item(
                                role["name"],
                                font_size="12px",
                                padding="2px 4px",
                                width="100%",
                            ),
                        ),
                    
                ),
                side="x",
                margin_top="24px",
                margin_bottom="24px",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Delete", color_scheme="red", on_click=RoleListState.delete_on_confirmation)
                ),
                rx.dialog.close(
                    rx.button("Cancel", variant="soft", color_scheme="gray", on_click=RoleListState.close_deletion_modal),
                ),
                spacing="3",
                justify="end",
            ),
            max_width="450px",
            width="95vw",
            padding="24px",
        ),
        open=RoleListState.show_deletion_modal,
    )
