import reflex as rx

from app.states.invite import InviteState
from app.models import invite as invite_models
from app.utils import Colors, btn_ghost_style, btn_primary_style


def invite_codes_content() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.flex(
                invite_add_button(),
                width="100%",
                padding="1em"
            ),
            invite_filters(),
            rx.flex(
                invite_list(),
                padding="1em",
                width="100%"
            ),
            padding="2em",
            background="#f5f7fb",
            width="100%"
        ),
        width="100%",
        padding="2em",
        background="#f5f7fb",
        min_height="100vh",
    )

def invite_add_button() -> rx.Component:
    return rx.flex(
        rx.button(
            rx.icon("plus", size=15),
            "Create Invite Code",
            on_click=InviteState.open_modal,
            **btn_primary_style,
        ),
        gap="1em",
        justify="end",
        align="start",
        width="100%"
    )

def invite_filters():
    return rx.box(
        rx.flex(
            rx.select(
                ["All", "Active", "Inactive"],
                value=InviteState.state,
                on_change=InviteState.set_state,
            ),
            rx.select(
                ["All", "Valid", "Expired", "Never"],
                value=InviteState.status,
                on_change=InviteState.set_status,
            ),
            justify="between",
            width="15%",
            wrap="wrap",
            spacing="2",
        ),

        bg="white",
        padding="20px",
        border_radius="12px",
        box_shadow="sm",
    )

def invite_table_header():
    return rx.hstack(
        rx.text("Code", font_weight="bold", width="22%"),
        rx.text("Expires", font_weight="bold", width="13%"),
        rx.text("Status", font_weight="bold", width="13%"),
        rx.text("Created At", font_weight="bold", width="13%"),
        rx.text("Created By", font_weight="bold", width="13%"),
        rx.text("Actions", font_weight="bold", width="13%"),
        padding="0.75em",
        border_bottom="1px solid #eaeaea",
    )

def invite_table():
    return rx.box(
        invite_table_header(),

        rx.foreach(
            InviteState.codes,
            invite_row,
        ),
        width="100%",
        border="1px solid #eaeaea",
        border_radius="10px",
        overflow="hidden",
        bg="white",
    )

def invite_actions_menu(invite: invite_models.InviteCodeRes):
    return rx.menu.root(
        rx.menu.trigger(
            rx.text("⋮", font_size="22px", cursor="pointer"),
        ),
        rx.menu.content(
            rx.menu.item(
                "View",
                # on_click=lambda: InviteState.modal_open(invite),
            ),
            rx.menu.item(
                "Edit",
                # on_click=lambda: AnnouncementListState.update_announcement(announcement),
            ),
            rx.menu.item(
                rx.cond(
                    invite.is_active,
                    "Deactivate",
                    "Activate"
                ),
                # on_click=lambda: AnnouncementListState.update_announcement(announcement),
            ),
            rx.menu.separator(),
            rx.menu.item(
                "Delete",
                # on_click=lambda: AnnouncementListState.delete_announcement(announcement["id"]),
                color="red",
            ),
        ),
    )

def invite_row(invite: invite_models.InviteCodeRes):
    return rx.hstack(
        rx.box(
            code_cell(invite.code),
            width='22%'
        ),
        rx.box(
            expires_cell(invite.expires_at, invite.expire_in),
            width="13%"
        ),
        rx.box(
            status_badge(invite.is_active),
            width="13%"
        ),
        rx.box(
            rx.moment(
                invite.created,
                format="MMM D, YYYY"
            ),
            width="13%"
        ),
        rx.box(
            rx.text(invite.created_by),
            width="13%"
        ),
        rx.box(
            invite_actions_menu(invite),
            width="13%"
        ),
        padding="0.75em",
        align="center",
        border_bottom="1px solid #f1f1f1",
    )

def invite_list():
    return rx.vstack(
        invite_table(),
        width="100%",
        spacing="4",
    )


def status_badge(is_active: bool) -> rx.Component:
    return rx.cond(
        is_active,
        rx.badge(
            "Active",
            color_scheme="green",
            variant="soft",
            radius="full",
            font_size="11.5px",
            font_weight="600",
        ),
        rx.badge(
            "Inactive",
            color_scheme="gray",
            variant="soft",
            radius="full",
            font_size="11.5px",
            font_weight="600",
        ),
    )

def code_cell(code: str) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.text(
                    code,
                    color=Colors.PURPLE,
                    font_weight="700",
                    font_size="13px",
                    font_family="monospace",
                    letter_spacing="0.03em",
                ),
                width="150px",
                height="40px",
                border_radius="5%",
                background=f"{Colors.PURPLE}15"
            ),
            rx.icon_button(
                rx.icon("copy", size=15),
                variant="ghost",
                size="1",
                cursor="pointer",
                on_click=InviteState.copy_code(code),
                title="Copy code",
            ),
            spacing="1",
            align="center",
        ),
        spacing="0",
        align="start",
    )

def expires_cell(expire_date: str, expire_in: str) -> rx.Component:
    return rx.vstack(
        rx.text(
            rx.cond(
                expire_date,
                rx.moment(
                    expire_date,
                    format="MMM D, YYYY"
                ),
                ""
            ),
            font_size="13px",
        ),
        rx.text(
            rx.cond(
                expire_in,
                expire_in,
                ""
            ),
            font_size="13px",
            color="gray",
        ),
        spacing="0",
        align="start",
    )