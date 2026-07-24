import reflex as rx
from app.states import role as role_states
from app.pages.components.form_label import form_label

from app.states import permission as permission_states


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
                    # announcement_delete_modal()
                ),
                rx.spacer(),
                role_filters(),
                bg="white",
                padding="20px",
                border_radius="12px",
                box_shadow="sm",
            ),
            rx.flex(
                # announcement_list(),
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