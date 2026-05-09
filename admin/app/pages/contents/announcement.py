import reflex as rx

from app.states.announcement import (
    AnnouncementFilterState,
    AnnouncementListState,
    AnnouncementState, 
    AnnouncementFormState, 
    AnnouncementTagState)
from app.states.status import StatusState
from app.states.audience import AudienceState
from app.pages.components.form_label import form_label
from app.pages.components.view_announcement import announcement_view_modal
from app.utils import get_short_desc


def church_announcement_card():
    return rx.flex(
        rx.box(
            rx.flex(
                announcement_add_buttons(),
                width="100%",
                padding="1em",
            ),
            announcement_filters(),
            rx.flex(
                announcement_list(),
                padding="1em",
                width="100%",
            ),
            
            padding="2em",
            background="#f5f7fb",
            width=rx.cond(
                AnnouncementState.show_add_update_drawer,
                "75%",   # shrink when drawer open
                "100%",
            ),
            transition="all 0.3s ease",
        ),

        # DRAWER
        announcement_add_update_drawer(),

        width="100%",
        padding="2em",
        background="#f5f7fb",
        min_height="100vh",
    )

def announcement_add_buttons():
    return rx.flex(
        rx.button(
            rx.icon("layout-template", size=18),
            "Templates",
            # on_click=lambda: rx.console_log("Open templates"),
            bg="#2d6cdf",
            color="white",
            padding="0.8em 1.2em",
            border_radius="10px",
            gap="0.5em",
            align="center",
        ),

        rx.button(
            rx.icon("plus", size=18),
            "Create Announcement",
            on_click=AnnouncementState.open_add_update_drawer,
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

def announcement_add_update_drawer():
    return rx.cond(
        AnnouncementState.show_add_update_drawer,
        rx.box(
            rx.flex(
                rx.box(
                    rx.flex(
                        rx.text("Create Announcement", font_weight="bold"),
                        rx.button(
                            rx.icon("x", size=18),
                            on_click=AnnouncementState.close_add_update_drawer,
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
                        announcement_form(),
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

def link_popup():
    return rx.cond(
        AnnouncementFormState.show_link_popup,
        rx.box(
            rx.box(
                # Header
                rx.flex(
                    rx.text("Add Link", font_weight="bold", font_size="1.1em"),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=AnnouncementFormState.toggle_link_popup,
                        bg="transparent",
                        color="gray",
                    ),
                    justify="between",
                    align="center",
                    mb="0.5em",
                ),
                # Form fields
                rx.box(
                    form_label('Title(Max 50)', text_color="#6b7280", font_weight="medium", required=True),
                    rx.input(
                        placeholder="e.g. Event Registration",
                        value=AnnouncementFormState.new_link_title,
                        on_change=AnnouncementFormState.set_new_link_title,
                        max_length=50,
                        required=True,
                        auto_focus=True
                    ),
                    mb="0.8em",
                ),

                rx.box(
                    form_label('URL', text_color="#6b7280", font_weight="medium", required=True),
                    rx.input(
                        placeholder="https://example.com",
                        value=AnnouncementFormState.new_link,
                        on_change=AnnouncementFormState.set_new_link,
                        required=True
                    ),
                ),

                # Actions
                rx.flex(
                    rx.button(
                        "Cancel",
                        on_click=AnnouncementFormState.toggle_link_popup,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button(
                        "Add Link",
                        on_click=AnnouncementFormState.add_link,
                        bg="#2563eb",
                        color="white",
                    ),
                    justify="end",
                    gap="0.5em",
                    mt="1em",
                ),

                padding="1.2em",
                bg="white",
                border_radius="12px",
                box_shadow="xl",
                width="350px",
            ),

            # overlay styling
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0,0,0,0.4)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="2000",
        ),
    )

def links_section():
    return rx.box(
        rx.hstack(
            rx.text("Links", font_weight="bold", size='1'),
            rx.text(f"(Max {AnnouncementFormState.max_links})", size="1"),
            spacing="0",
            justify="start",
            width="100%",
        ),

        rx.grid(
            rx.foreach(
                AnnouncementFormState.links,
                lambda link: rx.box(
                    rx.flex(
                        rx.link(
                            link['title'],
                            href=link['url'],
                            is_external=True,
                            font_size="0.6em"
                        ),
                        rx.button(
                            rx.icon("x", size=14),
                            on_click=lambda: AnnouncementFormState.remove_link(link),
                            bg="transparent",
                            color="gray",
                        ),
                        justify="between",
                        align="center",
                    ),
                    padding="0.2em",
                    border="1px solid #eee",
                    border_radius="8px",
                ),
            ),
            columns="2",
            gap="0.5em",
            padding_bottom="1em"
        ),

        rx.button(
            rx.icon("link", size=16),
            "Add Link",
            on_click=AnnouncementFormState.toggle_link_popup,
            bg="#f3f4f6",
            color="black",
            disabled=AnnouncementFormState.is_max_links_reached
        ),

        position="relative",
    )

def tags_section():
    available_tags = AnnouncementTagState.get_tags_name

    return rx.box(
        rx.text("Tags", font_weight="bold", size='1'),

        rx.flex(
            rx.foreach(
                available_tags,
                lambda tag: rx.checkbox(
                    tag,
                    checked=AnnouncementFormState.tags.contains(tag),
                    on_change=lambda _: AnnouncementFormState.toggle_tag(tag),
                    size="1",
                ),
            ),
            wrap="wrap",
            gap="1em",
            bg="#f9fafb",
            padding="1em",
            border_radius="10px",
            border="1px solid #e5e7eb",
            pt="0.5em",
        ),

        # Selected tags preview
        rx.flex(
            rx.foreach(
                AnnouncementFormState.tags,
                lambda tag: rx.box(
                    tag,
                    padding="0.3em 0.6em",
                    bg="#e0f2fe",
                    border_radius="6px",
                    font_size="0.8em",
                ),
            ),
            gap="0.5em",
            wrap="wrap",
            pt="0.5em",
        ),
    )

def audience_section():
    available_audiences = AudienceState.get_audience_name

    return rx.box(
        rx.text("Audiences", font_weight="bold", size='1'),

        rx.flex(
            rx.foreach(
                available_audiences,
                lambda audience: rx.checkbox(
                    audience,
                    checked=AnnouncementFormState.audiences.contains(audience),
                    on_change=lambda _: AnnouncementFormState.toggle_audience(audience),
                    size="1",
                ),
            ),
            wrap="wrap",
            gap="1em",
            bg="#f9fafb",
            padding="1em",
            border_radius="10px",
            border="1px solid #e5e7eb",
            pt="0.5em",
        ),

        # Selected audience preview
        rx.flex(
            rx.foreach(
                AnnouncementFormState.audiences,
                lambda audience: rx.box(
                    audience,
                    padding="0.3em 0.6em",
                    bg="#e0f2fe",
                    border_radius="6px",
                    font_size="0.8em",
                ),
            ),
            gap="0.5em",
            wrap="wrap",
            pt="0.5em",
        ),
    )

def rich_text_editor():
    # TODO: Replace with rich text editor

    return rx.text_area(
            placeholder="Content...",
            value=AnnouncementFormState.content,
            on_change=AnnouncementFormState.set_content,
            height="150px",
        ),

def announcement_form():
    return rx.box(
        rx.flex(
            form_label('Title', required=True),
            rx.box(
                rx.input(
                    placeholder="Baptism Service",
                    value=AnnouncementFormState.title,
                    on_change=AnnouncementFormState.set_title,
                    max_length=AnnouncementFormState.max_title_len,
                    auto_focus=True,
                    required=True
                ),
                rx.hstack(
                    rx.text(
                        AnnouncementFormState.get_title_len,
                        size="1",
                        color=rx.cond(
                            AnnouncementFormState.get_title_len
                            > AnnouncementFormState.max_title_len - 20,
                            "red",
                            "#111827",
                        ),
                    ),
                    rx.text("/", size="1"),
                    rx.text(
                        AnnouncementFormState.max_title_len,
                        size="1",
                        color="#6b7280",
                    ),
                    spacing="0",
                    justify="end",
                    width="100%",
                ),
            ),
            tags_section(),
            audience_section(),
            rx.hstack(
                rx.box(
                    form_label('Status', required=True),
                    rx.select(
                        StatusState.get_status_names,
                        value=AnnouncementFormState.status,
                        on_change=AnnouncementFormState.set_status,
                    ),
                    width="40%"
                ),
                rx.flex(
                    rx.text("Pin to Top", padding="0.5em", size='1'),
                    rx.switch(
                        checked=AnnouncementFormState.pin_to_top,
                        on_change=AnnouncementFormState.set_pin_to_top,
                    ),
                    align="center",
                    padding= "1em"
                )
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("Publish At", font_weight="bold", size='1'),
                    rx.input(
                        type="date",
                        value=AnnouncementFormState.publish_date,
                        on_change=AnnouncementFormState.set_publish_date,
                        disabled=AnnouncementFormState.toggle_publish_date_disable
                    ),
                ),
                rx.vstack(
                    rx.text("Expire At", font_weight="bold", size='1'),
                    rx.input(
                        type="date",
                        value=AnnouncementFormState.expire_date,
                        on_change=AnnouncementFormState.set_expire_date,
                        disabled=AnnouncementFormState.toggle_expire_date_disable,
                        border="1px solid",
                        border_color=rx.cond(
                            AnnouncementFormState.is_expire_date_greater_than_publish_date,
                            "white",
                            "#FF0000",
                        )
                    ),
                ),
            ),
            rx.text("Content", font_weight="bold", size='1'),
            rich_text_editor(),
            rx.fragment(
                links_section(),
                link_popup(),
            ),
            rx.hstack(
                rx.button(
                    rx.icon("trash_2", size=16),
                    "Reset",
                    on_click=AnnouncementFormState.reset_form,
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
                        AnnouncementFormState.id,
                        "Update",
                        "Create"
                    ),
                    bg = rx.cond(
                        AnnouncementFormState.id,
                        "blue.600",
                        "#10b981",
                    ),
                    on_click=AnnouncementFormState.submit,
                    color="white",
                    padding="0.8em 1.2em",
                    border_radius="10px",
                    gap="0.5em",
                    align="center",
                    disabled=AnnouncementFormState.toggle_submit_disable
                ),
                justify="between",
                width="100%"
            ),

            direction="column",
            gap="1em",
        ),
        padding="1em",
    )

def announcement_filters():
    return rx.box(
        rx.flex(
            rx.input(
                placeholder="🔍 Search announcements...",
                value=AnnouncementFilterState.search,
                on_change=AnnouncementFilterState.set_search,
                width="260px",
            ),

            rx.select(
                StatusState.get_status_names,
                value=AnnouncementFilterState.status,
                on_change=AnnouncementFilterState.set_status,
            ),

            rx.select(
                AudienceState.get_audience_name,
                value=AnnouncementFilterState.audience,
                on_change=AnnouncementFilterState.set_audience,
            ),

            rx.select(
                AnnouncementTagState.get_tags_name,
                value=AnnouncementFilterState.tag,
                on_change=AnnouncementFilterState.set_tag,
            ),

            justify="between",
            width="70%",
            wrap="wrap",
            spacing="4",
        ),

        bg="white",
        padding="20px",
        border_radius="12px",
        box_shadow="sm",
    )

def announcement_table_header():
    return rx.hstack(
        rx.checkbox(
            on_change=lambda _: AnnouncementListState.select_all()
        ),
        rx.text("Announcement", font_weight="bold", width="40%"),
        rx.text("Status", font_weight="bold", width="10%"),
        rx.text("Created By", font_weight="bold", width="10%"),
        rx.text("Published Date", font_weight="bold", width="20%"),
        rx.text("Actions", font_weight="bold", width="15%"),
        padding="0.75em",
        border_bottom="1px solid #eaeaea",
    )

def announcement_actions_menu(announcement):
    return rx.menu.root(
        rx.menu.trigger(
            rx.text("⋮", font_size="22px", cursor="pointer"),
        ),
        rx.menu.content(
            rx.menu.item(
                "View",
                on_click=lambda: AnnouncementListState.open_view_modal(announcement),
            ),
            rx.menu.item(
                "Edit",
                on_click=lambda: AnnouncementListState.update_announcement(announcement),
            ),
            rx.menu.sub(
                rx.menu.sub_trigger("Toggle Options"),
                rx.menu.sub_content(
                    rx.menu.item("Activate"),
                    rx.menu.item("Pin to Top"),
                ),
            ),
            rx.menu.separator(),
            rx.menu.item(
                "Delete",
                on_click=lambda: AnnouncementListState.delete_announcement(announcement["id"]),
                color="red",
            ),
        ),
    )

def tag_badge(tag: dict[str, str | bool]):
    return rx.box(
        tag.get('name', '-'),
        padding="2px 8px",
        border_radius="12px",
        font_size="8px",
        bg="#e8f0fe",
        color="#137333",
        margin_right="4px",
    )

link_badge = lambda link: rx.box(
    rx.link(
        link['title'],
            href=link['url'],
            is_external=True,
            #color="#2563eb",
        ),
        padding="2px 8px",
        border_radius="12px",
        font_size="8px",
        bg="#e6f4ea",
        color="#1a73e8",
        margin_right="4px",
)

def audience_badge(audience: dict[str, str | bool]):
    return rx.box(
        audience.get('name', '-'),
        padding="2px 8px",
        border_radius="12px",
        font_size="8px",
        bg="#e6f4ea",
        color="#010101",
        margin_right="4px",
    )

def get_announcement_item_name(item)-> str:
    return rx.cond(
        item,
        item['name'],
        "-"
    )

def announcement_row(announcement):
    short_desc = get_short_desc(announcement["content"], 100)
    return rx.hstack(
        # ✅ Checkbox
        rx.checkbox(
            checked=AnnouncementListState.selected_ids.contains(announcement["id"]),
            on_change=lambda _: AnnouncementListState.toggle_select(announcement["id"]),
        ),

        # 📄 Announcement (title + description)
        rx.box(
            rx.text(
                announcement["title"],
                font_weight="600",
                font_size="14px",
            ),
            rx.text(
                short_desc,
                font_size="13px",
                color="gray",
                no_of_lines=2,
            ),
            # Tags, audience and links section
            rx.hstack(
                rx.icon("tags", size=12, color="gray"),
                rx.foreach(
                    announcement["tags"],
                    tag_badge,
                ),
                rx.icon("users", size=12, color="gray"),
                rx.foreach(
                    announcement["audiences"],
                    audience_badge,
                ),
                rx.icon("link_2", size=12, color="gray"),
                rx.foreach(
                    announcement["links"],
                    link_badge,
                ),
                wrap="wrap",
                spacing="1",
            ),
            width="40%",
        ),

        # 📌 Status
        rx.box(
            rx.badge(
                get_announcement_item_name(announcement["status"]),
                color_scheme=rx.match(
                    get_announcement_item_name(announcement["status"]),
                    ("Published", "green"),
                    ("Draft", "gray"),
                    ("Expired", "red"),
                    ("Scheduled", "blue"),
                    "yellow",  # default
                ),
            ),
            width="10%",
        ),
        # 📅 Created By
        rx.box(
            rx.text(
                rx.cond(
                    announcement["creator"],
                    announcement["creator"]["first_name"],
                    "-"
                ),
                font_size="13px",
            ),
            width="10%",
        ),

        # 📅 Published Date
        rx.box(
            rx.text(
                rx.cond(
                    announcement["publish_at"],
                    rx.moment(
                        announcement["publish_at"],
                        format="MMM D, YYYY",
                    ),
                    "-"
                ),
                font_size="13px",
            ),
            width="20%",
        ),

        # ⚙️ Actions
        rx.box(
            rx.fragment(
                announcement_actions_menu(announcement),
                announcement_view_modal(),
            ),
            
            text_align="right",
        ),

        padding="0.75em",
        align="center",
        border_bottom="1px solid #f1f1f1",
    )

def announcement_table():
    return rx.box(
        announcement_table_header(),

        rx.foreach(
            AnnouncementListState.announcements,
            announcement_row,
        ),
        width="100%",
        border="1px solid #eaeaea",
        border_radius="10px",
        overflow="hidden",
        bg="white",
    )

def pagination_controls():
    return rx.hstack(
        rx.button(
            "Previous",
            on_click=AnnouncementListState.prev_page,
            disabled=AnnouncementListState.page == 1,
        ),

        rx.text(
            f"Page {AnnouncementListState.page} of {AnnouncementListState.total_pages}"
        ),

        rx.button(
            "Next",
            on_click=AnnouncementListState.next_page,
            disabled=AnnouncementListState.page == AnnouncementListState.total_pages,
        ),

        justify="end",
        width="100%",
        padding_top="1em",
    )

def announcement_list():
    return rx.vstack(
        announcement_table(),
        pagination_controls(),
        width="100%",
        spacing="4",
    )

