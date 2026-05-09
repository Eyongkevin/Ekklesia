import reflex as rx

from app.states.announcement import AnnouncementListState

def status_color(status):
    return rx.match(
        status,
        ("Published", "green"),
        ("Draft", "orange"),
        ("Expired", "red"),
        ("Scheduled", "blue"),
        "gray",
    )

def section_title(icon: str, title: str):
    return rx.hstack(
        rx.icon(
            icon,
            size=18,
            color="var(--accent-9)",
        ),

        rx.text(
            title,
            font_weight="600",
            size="3",
        ),

        spacing="2",
        align="center",
    )

def info_item(label: str, value):
    return rx.vstack(
        rx.text(
            label,
            size="2",
            color="gray",
            font_weight="500",
        ),

        value,

        spacing="1",
        align_items="start",
        width="100%",
    )

def announcement_view_modal():

    announcement = AnnouncementListState.selected_announcement

    return rx.dialog.root(

        rx.dialog.content(

            rx.vstack(

                # =========================
                # HEADER
                # =========================
                rx.hstack(

                    rx.vstack(

                        rx.heading(
                            announcement["title"],
                            size="6",
                        ),

                        rx.hstack(

                            rx.badge(
                                announcement["status"]["name"],
                                color_scheme=status_color(
                                    announcement["status"]["name"]
                                ),
                                radius="full",
                                size="2",
                            ),

                            rx.cond(
                                announcement["is_pinned"],
                                rx.badge(
                                    "Pinned",
                                    color_scheme="yellow",
                                    variant="soft",
                                ),
                            ),

                            spacing="2",
                        ),

                        align_items="start",
                        spacing="2",
                    ),

                    rx.spacer(),

                    rx.icon_button(
                        rx.icon("x"),
                        variant="ghost",
                        on_click=AnnouncementListState.close_view_modal,
                    ),

                    width="100%",
                    align="start",
                ),

                rx.divider(),

                # =========================
                # BODY
                # =========================
                rx.vstack(

                    # section_title(
                    #     "file-text",
                    #     "Announcement Body",
                    # ),

                    rx.box(
                        rx.cond(
                            announcement["content"],
                            rx.text(
                                announcement["content"],
                                white_space="pre-wrap",
                                line_height="1.8",
                                size="3",
                            ),
                            rx.text(
                                "No content provided.",
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

                # =========================
                # TAGS + AUDIENCES
                # =========================
                rx.grid(

                    # TAGS
                    rx.card(

                        rx.vstack(

                            section_title(
                                "tag",
                                "Tags",
                            ),

                            rx.flex(
                                rx.cond(
                                    announcement["tags"],
                                    rx.foreach(
                                        announcement["tags"],
                                        lambda tag: rx.badge(
                                            tag["name"],
                                            color_scheme="purple",
                                            variant="soft",
                                        ),
                                    ),
                                    rx.text(
                                        "No tags attached",
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

                    # AUDIENCES
                    rx.card(

                        rx.vstack(

                            section_title(
                                "users",
                                "Audiences",
                            ),

                            rx.flex(
                                rx.cond(
                                    announcement["audiences"],
                                    rx.foreach(
                                        announcement["audiences"],
                                        lambda audience: rx.badge(
                                            audience["name"],
                                            color_scheme="green",
                                            variant="soft",
                                        ),
                                    ),
                                    rx.text(
                                        "No audiences attached",
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

                    columns="2",
                    spacing="4",
                    width="100%",
                ),

                # =========================
                # LINKS
                # =========================
                rx.card(

                    rx.vstack(

                        section_title(
                            "link",
                            "Attached Links",
                        ),

                        rx.cond(

                            announcement["links"],

                            rx.vstack(

                                rx.foreach(
                                    announcement["links"],

                                    lambda link: rx.link(
                                        rx.hstack(

                                            rx.icon(
                                                "external-link",
                                                size=11,
                                            ),

                                            rx.text(
                                                link["title"],
                                                font_size="12px",
                                            ),

                                            spacing="2",
                                        ),

                                        href=link["url"],
                                        is_external=True,
                                        color="var(--accent-9)",
                                    ),
                                ),

                                spacing="3",
                                align_items="start",
                                width="100%",
                            ),

                            rx.text(
                                "No links attached",
                                color="gray",
                            ),
                        ),

                        spacing="4",
                        width="100%",
                        align_items="start",
                    ),

                    width="100%",
                ),

                # =========================
                # METADATA
                # =========================
                rx.card(

                    rx.vstack(

                        section_title(
                            "info",
                            "Announcement Information",
                        ),

                        rx.grid(

                            info_item(
                                "Created By",
                                rx.text(
                                    announcement["creator"]["first_name"],
                                    font_weight="600",
                                ),
                            ),
                            info_item(
                                "Published At",
                                rx.cond(
                                    announcement["publish_at"],
                                    rx.moment(
                                        announcement["publish_at"],
                                        format="MMM DD, YYYY",
                                    ),
                                    rx.text("N/A"),
                                
                                )
                            ),
                            info_item(
                                "Expired At",
                                rx.cond(
                                    announcement["expire_at"],
                                    rx.moment(
                                        announcement["expire_at"],
                                        format="MMM DD, YYYY",
                                    ),
                                    rx.text("N/A"),
                                
                                )
                            ),

                            info_item(
                                "Created At",

                                rx.moment(
                                    announcement["created_at"],
                                    format="MMM DD, YYYY • hh:mm A",
                                ),
                            ),

                            info_item(
                                "Modified At",

                                rx.moment(
                                    announcement["modified_at"],
                                    format="MMM DD, YYYY • hh:mm A",
                                ),
                            ),

                            columns="5",
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

                # =========================
                # FOOTER
                # =========================
                rx.flex(
                    rx.hstack(
                        # DELETE
                        rx.button(
                            rx.icon("trash-2", size=16),
                            rx.text("Delete"),

                            color_scheme="red",
                            variant="soft",

                            on_click=lambda: AnnouncementListState.delete_announcement(
                                announcement["id"]
                            ),

                            spacing="2",
                        ),
                        # UPDATE
                        rx.button(
                            rx.icon("square-pen", size=16),
                            rx.text("Update"),

                            color_scheme="blue",

                            on_click=lambda: AnnouncementListState.update_announcement(
                                announcement
                            ),

                            spacing="2",
                        ),
                        # PIN/UNPIN
                        rx.button(
                            rx.cond(
                                announcement["is_pinned"],
                                rx.icon("pin_off", size=16),
                                rx.icon("pin", size=16),
                            ),
                            rx.cond(
                                announcement["is_pinned"],
                                rx.text("Unpin"),
                                rx.text("Pin"),
                            ),
                            color_scheme="yellow",

                            # on_click=lambda: AnnouncementListState.open_update_modal(
                            #     announcement
                            # ),

                            spacing="2",
                        ),

                        spacing="3",

                    ),

                    rx.spacer(),

                    # CANCEL
                    rx.button(
                        "Close",
                        variant="soft",
                        on_click=AnnouncementListState.close_view_modal,
                    ),

                    width="100%",
                    align="center",
                ),

                spacing="5",
                width="100%",
                align_items="start",
            ),

            max_width="850px",
            width="95vw",
            padding="24px",
        ),
        open=AnnouncementListState.show_view_modal,
    )