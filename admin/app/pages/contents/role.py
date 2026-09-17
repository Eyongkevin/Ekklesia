import reflex as rx
from app.states import role as role_states
from app.pages.components.form_label import form_label
from app.pages.components.list_components import status_icon

from app.states import permission as permission_states
from app.utils import get_short_desc
from app.pages.components.view_announcement import section_title, info_item
from app.pages.components.role import delete_confirmation_modal


def role_card():
    return rx.flex(
        rx.box(
            rx.flex(
                role_add_buttons(),
                width="100%",
                padding="1em",
            ),
            rx.hstack(
                rx.fragment(
                    role_actions(),
                    delete_confirmation_modal(),
                    role_view_modal()
                ),
                rx.spacer(),
                role_filters(),
                bg="white",
                padding="20px",
                border_radius="12px",
                box_shadow="sm",
            ),
            rx.flex(
                role_list(),
                padding="1em",
                width="100%",
            ),
            
            padding="2em",
            background="#f5f7fb",
            width=rx.cond(
                role_states.RoleState.show_add_update_drawer,
                "75%",   # shrink when drawer open
                "100%",
            ),
            transition="all 0.3s ease",
        ),

        # DRAWER
        role_add_update_drawer(),


        width="100%",
        padding="2em",
        background="#f5f7fb",
        min_height="100vh",
    )

def role_add_buttons():
    return rx.flex(
        rx.button(
            rx.icon("plus", size=18),
            "Create Role",
            on_click= role_states.RoleState.open_add_update_drawer,
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

def role_actions():
    return rx.select(
        ["Delete selected items"],
        # value=AnnouncementListState.actions_value,
        # on_change=AnnouncementListState.on_select_actions,
        color_scheme="red",
        placeholder="Actions",
    )

def role_filters():
    return rx.box(
        rx.flex(
            rx.input(
                placeholder="🔍 Search roles...",
                value=role_states.RoleFilterState.search,
                on_change=role_states.RoleFilterState.set_search,
                width="260px",
            ),
            justify="between",
            width="100%",
            wrap="wrap",
            spacing="4",
        ),
    )

def role_add_update_drawer():
    return rx.cond(
        role_states.RoleState.show_add_update_drawer,
        rx.box(
            rx.flex(
                rx.box(
                    rx.flex(
                        rx.text("Create Role", font_weight="bold"),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=role_states.RoleState.close_add_update_drawer,
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
                        role_form(),
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

def permission_item(permission: str) -> rx.Component:
    return rx.checkbox(
        permission,
        checked=role_states.RoleFormState.selected_permissions.contains(permission),
        on_change=lambda _:role_states.RoleFormState.toggle_permission_select(permission),
        size="2",
    )

def permission_group(title: str, permissions: list[str]) -> rx.Component:
    return rx.accordion.item(
        header=rx.hstack(
            rx.icon("shield-check", size=16),
            rx.text(title, size='1'),
            spacing="2",
        ),
        content=rx.vstack(
            rx.foreach(
                permissions,
                permission_item
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        value=title,
        # style={
        #     "background_color": "#767373",
        #     "border": "1px solid #e5e7eb",
        #     "border_radius": "8px",
        # },
    )

def permissions_panel() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                form_label('Permissions', required=True),
                rx.spacer(),
                rx.input(
                    placeholder="Search permissions...",
                    width="250px",
                ),
                width="100%",
            ),

            rx.accordion.root(
                rx.foreach(
                    permission_states.PermissionState.permissions_group.items(),
                    lambda item: permission_group(
                        item[0],
                        item[1],
                    ),
                ),
                type="multiple",
                width="100%",
            ),

            spacing="3",
            width="100%",
        ),
        width="100%",
    )

def role_form():
    return rx.box(
        rx.flex(
            form_label('Name', required=True),
            rx.box(
                rx.input(
                    placeholder="Senior Pastor",
                    value=role_states.RoleFormState.name,
                    on_change=role_states.RoleFormState.set_name,
                    max_length=role_states.RoleFormState.max_name_len,
                    auto_focus=True,
                    required=True
                ),
                rx.hstack(
                    rx.text(
                        role_states.RoleFormState.get_name_len,
                        size="1",
                        color=rx.cond(
                            role_states.RoleFormState.get_name_len
                            > role_states.RoleFormState.max_name_len - 20,
                            "red",
                            "#111827",
                        ),
                    ),
                    rx.text("/", size="1"),
                    rx.text(
                        role_states.RoleFormState.max_name_len,
                        size="1",
                        color="#6b7280",
                    ),
                    spacing="0",
                    justify="end",
                    width="100%",
                ),
            ),
            permissions_panel(),
            rx.text("Description", font_weight="bold", size='1'),
            rx.text_area(
                placeholder="Leads the church, provides spiritual oversight....",
                value=role_states.RoleFormState.description,
                on_change=role_states.RoleFormState.set_description,
                height="100px",
            ),
            rx.hstack(
                rx.button(
                    rx.icon("trash_2", size=16),
                    "Reset",
                    on_click=role_states.RoleFormState.reset_form,
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
                        role_states.RoleFormState.id,
                        "Update",
                        "Create"
                    ),
                    bg = rx.cond(
                        role_states.RoleFormState.id,
                        "blue.600",
                        "#10b981",
                    ),
                    on_click=role_states.RoleFormState.submit,
                    color="white",
                    padding="0.8em 1.2em",
                    border_radius="10px",
                    gap="0.5em",
                    align="center",
                    disabled=role_states.RoleFormState.toggle_submit_disable
                ),
                justify="between",
                width="100%"
            ),

            direction="column",
            gap="1em",
        ),
        padding="1em",
    )


def role_table_header():
    return rx.hstack(
        rx.text("Role", font_weight="bold", width="30%", size="2"),
        rx.text("From system", font_weight="bold", width="10%", size="2"),
        rx.text("Version", font_weight="bold", width="5%", size="2"),
        rx.text("Active", font_weight="bold", width="5%", size="2"),
        rx.text("Customized", font_weight="bold", width="10%", size="2"),
        rx.text("Created At", font_weight="bold", width="10%", size="2"),
        rx.text("Created By", font_weight="bold", width="20%", size="2"),
        rx.text("Actions", font_weight="bold", width="10%", size="2"),
        padding="0.75em",
        border_bottom="1px solid #eaeaea",
    )

def role_table():
    return rx.box(
        role_table_header(),

        rx.foreach(
            role_states.RoleListState.roles,
            role_row,
        ),
        width="100%",
        border="1px solid #eaeaea",
        border_radius="10px",
        overflow="hidden",
        bg="white",
    )

def role_row(role):
    short_desc = get_short_desc(role["description"], 100)
    return rx.hstack(

        # 📄 Role (name + description)
        rx.box(
            rx.text(
                role["name"],
                font_weight="600",
                font_size="14px",
            ),
            rx.text(
                short_desc,
                font_size="13px",
                color="gray",
                no_of_lines=2,
            ),
            width="30%",
        ),

        # 📌 From System
        rx.box(
            status_icon(role['system_role_id'] != None),
            width="9%",

        ),

        # 📌 Version
        rx.box(
            rx.text(role['template_version']),
            width="4%",
        ),

        # 📌 Active
        rx.box(
            status_icon(role['is_active']),
            width="6%",
        ),

        # 📌 Customized
        rx.box(
            status_icon(role['is_customized']),
            width="7%",
        ),

        # 📅 Created At
        rx.box(
            rx.text(
                rx.cond(
                    role["created_at"],
                    rx.moment(
                        role["created_at"],
                        format="MMM D, YYYY",
                    ),
                    "-"
                ),
                font_size="13px",
            ),
            width="10%",
        ),
        
        # 📅 Created By
        rx.box(
            rx.text(
                "Kevin Enow",
                font_size="13px",
            ),
            width="19%",
        ),

        # ⚙️ Actions
        rx.box(
            rx.fragment(
                role_actions_menu(role),
                # role_view_modal(),
            ),
            text_align="right",
        ),
        padding="0.75em",
        align="center",
        border_bottom="1px solid #f1f1f1",
    )

def role_actions_menu(role):
    return rx.menu.root(
        rx.menu.trigger(
            rx.text("⋮", font_size="22px", cursor="pointer"),
        ),
        rx.menu.content(
            rx.menu.item(
                "View",
                on_click=lambda: role_states.RoleListState.open_view_modal(role),
            ),
            rx.cond(
                role['is_protected'],
                rx.menu.item("Edit", disabled=True),
                rx.menu.item(
                    "Edit",
                    on_click=lambda: role_states.RoleListState.update_role(role),
                ),
            ),
            rx.menu.item(
                "Activate",
                # on_click=lambda: AnnouncementListState.update_announcement(announcement),
            ),
            rx.menu.separator(),
            rx.cond(
                role['is_protected'],
                rx.menu.item("Delete", disabled=True, color="red"),
                rx.menu.item(
                    "Delete",
                    on_click=lambda: role_states.RoleListState.delete(role),
                    color="red",
                ),
            ),
        ),
    )

def role_view_modal():
    role = role_states.RoleListState.selected_role

    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            role["name"],
                            size="6",
                        ),
                        align_items="start",
                        spacing="2",
                    ),

                    rx.spacer(),

                    rx.icon_button(
                        rx.icon("x"),
                        variant="ghost",
                        on_click=role_states.RoleListState.close_view_modal,
                    ),

                    width="100%",
                    align="start",
                ),

                rx.divider(),

                rx.vstack(
                    rx.box(
                        rx.cond(
                            role["description"],
                            rx.text(
                                role["description"],
                                white_space="pre-wrap",
                                line_height="1.8",
                                size="3",
                            ),
                            rx.text(
                                "No description.",
                                color="gray",
                            ),
                        ),
                        bg="var(--gray-2)",
                        padding="18px",
                        border_radius="12px",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                    align_items="start",
                ),
                rx.card(
                    rx.vstack(
                        section_title(
                            "user-key",
                            "Permissions",
                        ),

                        rx.flex(
                            rx.cond(
                                role["permissions"],
                                rx.foreach(
                                    role["permissions"],
                                    lambda permission: rx.badge(
                                        permission["name"],
                                        color_scheme="purple",
                                        variant="soft",
                                    ),
                                ),
                                rx.text(
                                    "No permissions",
                                    color="gray",
                                ),
                            ),

                            wrap="wrap",
                            spacing="2",
                        ),
                        spacing="4",
                        width="100%",
                        align_items="start",
                    ),
                    width="100%",
                ),
                rx.card(
                    rx.vstack(

                        section_title(
                            "info",
                            "Role Information",
                        ),

                        rx.grid(

                            info_item(
                                "Created By",
                                rx.text(
                                    "-",
                                    font_weight="600",
                                ),
                            ),
                            info_item(
                                "Created At",

                                rx.moment(
                                    role["created_at"],
                                    format="MMM DD, YYYY • hh:mm A",
                                ),
                            ),

                            info_item(
                                "Modified At",

                                rx.moment(
                                    role["modified_at"],
                                    format="MMM DD, YYYY • hh:mm A",
                                ),
                            ),

                            columns="3",
                            spacing="2",
                            width="100%",
                            font_size="12px",
                        ),

                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),

                    width="100%",
                ),
                rx.flex(
                    rx.hstack(
                        # DELETE
                        rx.button(
                            rx.icon("trash-2", size=16),
                            rx.text("Delete"),
                            color_scheme="red",
                            variant="soft",
                            on_click=lambda: role_states.RoleListState.delete(role),
                            disabled=role['is_protected'],
                            spacing="2",
                        ),
                        # UPDATE
                        rx.button(
                            rx.icon("square-pen", size=16),
                            rx.text("Update"),

                            color_scheme="blue",

                            on_click=lambda: role_states.RoleListState.update_role(
                                role
                            ),
                            disabled=role['is_protected'],

                            spacing="2",
                        ),
                        spacing="3",
                    ),

                    rx.spacer(),

                    # CANCEL
                    rx.button(
                        "Close",
                        variant="soft",
                        on_click=role_states.RoleListState.close_view_modal,
                    ),

                    width="100%",
                    align="center",
                ),
            )
        ),
        open=role_states.RoleListState.show_view_modal
    )

def role_before_deletion_modal():
    role = role_states.RoleListState.roles_to_be_deleted
    users_first_name = role_states.RoleListState.users_first_name

    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.icon("triangle-alert", size=30, color="red"),
                rx.heading("Please Confirm", size="4"),
                rx.dialog.description(
                    rx.text(
                        "The role ",
                        rx.text.span(
                            role[0]["name"],
                            color="#60A5FA",
                            # font_weight="bold",
                        ),
                        f" is assigned to {users_first_name.length()} user(s).",
                    ),
                    rx.text(
                        "Replace the role before you can delete it", 
                        size="1", 
                        color="#D10D0D",
                        align="center"
                    )
                ),
                align="center"
            ),
            rx.flex(
                rx.inset(
                    rx.list.unordered(
                        rx.foreach(
                            users_first_name,
                            lambda first_name: rx.list.item(
                                first_name,
                                font_size="12px",
                                padding="2px 4px",
                                width="100%",
                            ),
                        ),
                        
                    ),
                    side="x",
                    margin_top="24px",
                    margin_bottom="24px"
                ),
                width="100%",
                margin_left="40px"
                #justify="center",
            ),
            
            rx.flex(
                rx.select(
                    role_states.RoleListState.get_all_role_names,
                    value=role_states.RoleListState.role_name_to_be_replaced_with,
                    on_change=role_states.RoleListState.set_role_name_to_be_replaced_with,
                    placeholder="Replace with…",
                ),
                margin_bottom="24px",
                width="100%",
                justify="center",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Replace & Delete", 
                        color_scheme="red",
                        disabled=role_states.RoleListState.role_name_to_be_replaced_with_is_not_set,
                        # on_click= role_states.RoleListState.merge_role
                        )
                ),
                rx.dialog.close(
                    rx.button("Cancel", variant="soft", color_scheme="gray", on_click=role_states.RoleListState.close_before_deletion_modal),
                ),
                spacing="3",
                justify="end",
            ),
            max_width="450px",
            width="95vw",
            padding="24px",
        ),
        open=role_states.RoleListState.show_before_deletion_modal,
    )

def role_list():
    return rx.vstack(
        role_table(),
        # pagination_controls(AnnouncementListState),
        width="100%",
        spacing="4",
    )
