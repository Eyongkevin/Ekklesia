import reflex as rx
from app.states import user as user_states
from app.states import role as role_states
from app.pages.components.form_label import form_label
from app.pages.components.list_components import status_icon

from app.states import permission as permission_states
from app.utils import get_short_desc, format_created_by
from app.pages.components.view_announcement import section_title, info_item
from app.pages.components.role import delete_confirmation_modal


def user_card():
    return rx.flex(
        rx.box(
            rx.flex(
                user_add_buttons(),
                width="100%",
                padding="1em",
            ),
            rx.hstack(
                rx.fragment(
                    user_actions(),
                    # delete_confirmation_modal(),
                    # role_view_modal()
                ),
                rx.spacer(),
                user_filters(),
                bg="white",
                padding="20px",
                border_radius="12px",
                box_shadow="sm",
            ),
            rx.flex(
                user_list(),
                padding="1em",
                width="100%",
            ),
            
            padding="2em",
            background="#f5f7fb",
            width= "100%", # =rx.cond(
            #     role_states.RoleState.show_add_update_drawer,
            #     "75%",   # shrink when drawer open
            #     "100%",
            # ),
            transition="all 0.3s ease",
        ),

        # DRAWER
        # role_add_update_drawer(),


        width="100%",
        padding="2em",
        background="#f5f7fb",
        min_height="100vh",
    )

def user_add_buttons():
    return rx.flex(
        rx.button(
            rx.icon("plus", size=18),
            "Create User",
            # on_click= role_states.RoleState.open_add_update_drawer,
            bg="#10b981",
            color="white",
            padding="0.8em 1.2em",
            border_radius="10px",
            gap="0.5em",
            align="center",
        ),

        gap="1em",
        justify="end",
        align="start",
        width="100%"
    )

def user_actions():
    return rx.select(
        ["Delete selected items"],
        # value=AnnouncementListState.actions_value,
        # on_change=AnnouncementListState.on_select_actions,
        color_scheme="red",
        placeholder="Actions",
    )

def user_filters():
    return rx.box(
        rx.flex(
            rx.hstack(
                rx.text("Active"),
                rx.select(
                    ["All", "True", "False"],
                    value=user_states.UserAdminFilterState.is_active,
                    on_change=user_states.UserAdminFilterState.set_is_active
                ),
            ),
            rx.hstack(
                rx.text("Roles"),
                rx.select(
                    role_states.RoleState.get_roles_name,
                    value=user_states.UserAdminFilterState.role,
                    on_change=user_states.UserAdminFilterState.set_role
                ),
            ),
            rx.input(
                placeholder="🔍 Search users...",
                value=user_states.UserAdminFilterState.search,
                on_change=user_states.UserAdminFilterState.set_search,
                width="260px",
            ),
            justify="between",
            width="100%",
            wrap="wrap",
            spacing="4",
        ),
    )

def user_table_header():
    return rx.hstack(
        rx.text("First Name", font_weight="bold", width="15%", size="2"),
        rx.text("Last Name", font_weight="bold", width="15%", size="2"),
        rx.text("Email", font_weight="bold", width="15%", size="2"),
        rx.text("Assigned Roles", font_weight="bold", width="30%", size="2"),
        rx.text("Status", font_weight="bold", width="10%", size="2"),
        rx.text("Created At", font_weight="bold", width="20%", size="2"),
        rx.text("Created By", font_weight="bold", width="20%", size="2"),
        rx.text("Actions", font_weight="bold", width="10%", size="2"),
        padding="0.75em",
        border_bottom="1px solid #eaeaea",
    )

def user_table():
    return rx.box(
        user_table_header(),

        rx.foreach(
            user_states.UserAdminListState.admins,
            admin_row,
        ),
        width="100%",
        border="1px solid #eaeaea",
        border_radius="10px",
        overflow="hidden",
        bg="white",
    )

def user_list():
    return rx.vstack(
        user_table(),
        width="100%",
        spacing="4",
    )

def role_badge(role: dict[str, str | bool]):
    return rx.box(
        role.get('name', '-'),
        padding="1px 6px",
        border_radius="12px",
        font_size="8px",
        bg="#e8f0fe",
        color="#191373",
        margin_right="1px",
    )

def admin_row(admin):
    return rx.hstack(

        # 📄 First name
        rx.box(
            rx.text(
                admin["first_name"],
                font_weight="600",
                font_size="14px",
            ),
            width="15%",
        ),
        # Last name
        rx.box(
            rx.text(
                admin["last_name"],
                font_weight="600",
                font_size="14px",
            ),
            width="15%",
        ),

        # Email
        rx.box(
            rx.text(
                admin["email"],
                font_weight="600",
                font_size="14px",
            ),
            width="15%",
        ),

        # 📌 Roles
        rx.box(
            rx.flex(
                rx.icon("briefcase-business", size=12, color="gray"),
                rx.foreach(
                    admin["memberships"][0]["roles"],
                    role_badge,
                ),
                wrap="wrap",
                spacing="2",
                align="center",
            ),
            width="30%",
            min_width="0",
        ),

        # 📌 Active
        rx.box(
            status_icon(admin['is_active']),
            width="10%",
        ),

        # 📅 Created At
        rx.box(
            rx.text(
                rx.cond(
                    admin["created_at"],
                    rx.moment(
                        admin["created_at"],
                        format="MMM D, YYYY",
                    ),
                    "-"
                ),
                font_size="13px",
            ),
            width="20%",
        ),
        
        # 📅 Created By
        rx.box(
            rx.text(
                admin["created_by_name"],
                font_size="13px",
            ),
            width="20%",
        ),

        # ⚙️ Actions
        rx.box(
            rx.fragment(
                # role_actions_menu(role),
                # role_view_modal(),
            ),
            text_align="right",
            width="10%"
        ),
        padding="0.75em",
        align="center",
        border_bottom="1px solid #f1f1f1",
    )