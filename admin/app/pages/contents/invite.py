import reflex as rx

from app.states.invite import InviteState, InviteFormState, InvitetListState, InviteType, InviteFilterState
from app.models import invite as invite_models
from app.utils import Colors, btn_ghost_style, btn_primary_style
from app.pages.components.form_label import form_label
from app.pages.components.pagination_control import pagination_controls
from app.states.status import StatusState


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
            width=rx.cond(
                InviteState.show_add_update_drawer,
                "75%",
                "100%"
            ),
            transition="all 0.3s ease"
        ),

        # DRAWER
        invite_add_update_drawer(),

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
            on_click=InviteState.open_add_update_drawer,
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
                value=InviteFilterState.is_active,
                on_change=InviteFilterState.set_is_active,
            ),
            rx.select(
                ["All", "Valid", "Expired", "Never"],
                value=InviteFilterState.state,
                on_change=InviteFilterState.set_state,
            ),
            justify="between",
            width="22%",
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
        rx.text("Created By", font_weight="bold", width="20%"),
        rx.text("Actions", font_weight="bold", width="15%"),
        padding="0.75em",
        border_bottom="1px solid #eaeaea",
    )

def invite_table():
    return rx.box(
        invite_table_header(),

        rx.foreach(
            InvitetListState.invites,
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
                "Edit",
                on_click=lambda: InvitetListState.prefil_form_for_update(invite),
            ),
            rx.menu.item(
                rx.cond(
                    invite.is_active,
                    "Deactivate",
                    "Activate"
                ),
                on_click=lambda: InvitetListState.update_invite_state(invite),
            ),
            rx.menu.separator(),
            rx.menu.item(
                "Delete",
                on_click=lambda: InvitetListState.delete(invite["id"]),
                color="red",
            ),
        ),
    )

def invite_row(invite: InviteType):
    return rx.hstack(
        rx.box(
            code_cell(invite["code"]),
            width='22%'
        ),
        rx.box(
            expires_cell(invite["expires_at"], invite["expire_in"]),
            width="13%"
        ),
        rx.box(
            status_badge(invite["is_active"]),
            width="13%"
        ),
        rx.box(
            rx.moment(
                invite["created_at"],
                format="MMM D, YYYY"
            ),
            width="13%"
        ),
        rx.box(
            rx.text(invite["creator"]["first_name"]),
            width="20%"
        ),
        rx.box(
            invite_actions_menu(invite),
            text_align="right"
        ),
        padding="0.75em",
        align="center",
        border_bottom="1px solid #f1f1f1",
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
                on_click=InvitetListState.copy_code(code),
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
            color=rx.cond(
                expire_in == "(Expired)",
                "#B71C1C",  # Dark red
                rx.cond(
                    expire_in == "Never",
                    "#424242",  # Dark gray
                    "#1B5E20"   # Dark green (valid)
                )
            ),
            bg=rx.cond(
                expire_in == "(Expired)",
                "#FDECEC",  # Light red
                rx.cond(
                    expire_in == "Never",
                    "#F1F3F4",  # Light gray
                    "#E8F5E9"   # Light green
                )
            ),
        ),
        spacing="0",
        align="start",
    )

def invite_add_update_drawer():
    return rx.cond(
        InviteState.show_add_update_drawer,
        rx.box(
            rx.flex(
                rx.box(
                    rx.flex(
                        rx.text("Create Invite Code", font_weight="bold"),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=InviteState.close_add_update_drawer,
                            bg="transparent",
                            color="#6b7280",
                            border_radius="6px",
                            _hover={"bg": "#f3f4f6"},
                        ),
                        justify="between",
                        align="center",
                        padding="1em",
                        padding_bottom="1.5em",
                        border_bottom="1px solid #eee",
                    ),

                    rx.box(
                        invite_form(),
                        padding="1em",
                        flex="1",
                        overflow_y="auto",
                    ),

                    display="flex",
                    flex_direction="column",
                    height="100%",
                    width="100%",
                    bg="white",
                ),

                position="fixed",
                top="0",
                right="0",
                height="100vh",
                width="25%",
                bg="white",
                box_shadow="lg",
                z_index="1000",
            ),
        ),
    )

def invite_form():
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.box(
                    form_label('State', required=True),
                    rx.select(
                        ["Active", "Inactive"],
                        value=InviteFormState.state,
                        on_change=InviteFormState.set_state,
                    ),
                    width="40%",
                    columns=2,
                ),
                rx.hstack(
                    rx.text("Expire At", font_weight="bold", size='1'),
                    rx.input(
                        type="date",
                        value=InviteFormState.expire_date,
                        on_change=InviteFormState.set_expire_date,
                        border="1px solid",
                        border_color=rx.cond(
                            InviteFormState.is_expire_date_lesser_than_today_date,
                            "#FF0000",
                            "white",
                            
                        )
                    ),
                    rx.input(
                        type="time",
                        value=InviteFormState.expire_time,
                        on_change=InviteFormState.set_expire_time,
                        border="1px solid",
                        border_color=rx.cond(
                            InviteFormState.is_expire_time_lesser_than_today_time,
                            "#FF0000",
                            "white",
                        ),
                        # disabled=InviteFormState.toggle_disable_expire_time
                    ),
                ),
            ),
            rx.hstack(
                rx.icon("shield-check", size=36, color=Colors.PURPLE),
                rx.vstack(
                    rx.text("How invite codes work", font_weight="bold", size="2"),
                    rx.text("Share this code with people you want to invite. They can use it during sign up to join your church", size="1"),
                    align="start",
                    spacing="0",
                ),
                padding="1.2em",
                border_radius="5%",
                background=f"{Colors.PURPLE}15",
            ),
            rx.vstack(
                rx.text("Preview"),
                rx.box(
                    rx.hstack(
                        rx.center(
                            rx.text(
                                InviteFormState.church_code,
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
                        rx.center(
                            rx.text(
                                '-',
                                font_weight="700",
                                font_size="20px",
                                font_family="monospace",
                                letter_spacing="0.03em",
                        ),
                        height="45px"
                        ),                   
                        rx.center(
                            rx.text(
                                InviteFormState.code,
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
                        rx.button(
                            rx.icon("refresh-cw", size=16),
                            on_click=InviteFormState.generate_code(),
                            disabled=InviteFormState.id != "",
                            bg="transparent",
                            color="gray",
                        ),
                    ),
                )
            ),
            rx.text(
                "The full code will be generated when you create it.",
                font_size="13px",
                color="gray",
            ),
            rx.hstack(
                rx.button(
                    rx.icon("trash_2", size=16),
                    "Reset",
                    on_click=InviteFormState.reset_form,
                    bg="#ffffff",
                    color="#fa2d2d",
                    border="1px solid",
                    border_color="#fa2d2d",
                    padding="0.8em 1.2em",
                    border_radius="10px",
                    gap="0.5em",
                    align="center",
                ),
                rx.button(
                    rx.cond(
                        InviteFormState.id,
                        "Update",
                        "Create"
                    ),
                    bg = rx.cond(
                        InviteFormState.id,
                        "blue.600",
                        "#10b981",
                    ),
                    on_click= rx.cond(
                        InviteFormState.id,
                        InviteFormState.update,
                        InviteFormState.create
                    ),
                    disabled = InviteFormState.is_expire_date_lesser_than_today_date | InviteFormState.is_expire_time_lesser_than_today_time | InviteFormState.is_time_set_but_date_not_set,
                    color="white",
                    padding="0.8em 1.2em",
                    border_radius="10px",
                    gap="0.5em",
                    align="center",
                ),
                justify="between",
                width="100%"
            ),

            direction="column",
            gap="1em",
        ),
        padding="1em",
    )

def invite_list():
    return rx.vstack(
        invite_table(),
        pagination_controls(InvitetListState),
        width="100%",
        spacing="4",
    )

