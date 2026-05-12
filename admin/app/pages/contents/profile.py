import reflex as rx

from app.states import (
    theme as theme_states,
    membership as membership_states,
    church as church_states,
    contact as contact_states
)

def stat_item(label: str, value: str, icon_text: str = "", icon_color: str = "gray"):
    return rx.hstack(
        rx.cond(
            icon_text,
            rx.center(
                rx.icon(
                    icon_text,
                    size=18,
                    color=icon_color,
                ),
                width="42px",
                height="42px",
                border_radius="50%",
                background=f"{icon_color}15"
            ),
        ),
        rx.vstack(
            rx.text(value, font_size="1.3em", font_weight="bold", line_height="1.5"),
            rx.text(label, font_size="0.8em", color="gray", line_height="1.5"),
            align="start",
            spacing="0",
        ),
        spacing="2",
        align="center",
    )

def list_item(label: str, icon_text: str = "", icon_color: str = "gray"):
    return rx.hstack(
        rx.cond(
            icon_text,
            rx.center(
                rx.icon(
                    icon_text,
                    size=18,
                    color=icon_color,
                ),
                width="30px",
                height="30px",
                border_radius="50%",
                background=f"{icon_color}15"
            ),
        ),
        rx.text(label, font_size="0.8em", line_height="1.5"),
        spacing="2",
        align="center",
    )

def section_card(
        title: str, 
        content, 
        no_padding: bool = False, 
        action=None, 
        icon_text: str = "",
        icon_color: str = "gray"):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.cond(
                    icon_text,
                    rx.icon(icon_text, size=28, color=icon_color),
                ),
                rx.cond(
                    title,
                    rx.heading(title, size="4"),
                ),
                rx.cond(
                    action,
                    rx.hstack(
                        rx.spacer(),
                        action
                    ),
                    rx.box()
                )
            ),
            content,
            spacing="3",
            align="start",
        ),
        padding="0" if no_padding else "1.5em",
        border_radius="16px",
        box_shadow="0 2px 10px rgba(0,0,0,0.06)",
        background="white",
        width="100%",
        min_width="220px",
        overflow="hidden",
    )

def stat_group(title: str, *items, icon_text: str = "", icon_color: str = "gray", columns="3"):
    return rx.vstack(
        rx.hstack(
            rx.cond(
                icon_text,
                rx.icon(icon_text, size=24, color=icon_color),
            ),
            rx.heading(title, size="2"),
        ),
        # rx.text(
        #     title,
        #     font_weight="bold",
        #     color="gray",
        #     font_size="0.9em",
        # ),
        rx.grid(
            *items,
            columns=columns,
            spacing="3",
            width="100%",
        ),
        spacing="2",
        align="start",
        width="100%",
    )

def edit_button(action):
    return rx.icon_button(
        "pencil",
        size="2",
        variant="ghost",
        on_click=action,
    )

def profile_section():
    return section_card(
        None,
        rx.box(
            rx.image(
                src="https://images.unsplash.com/photo-1507692049790-de58290a4334?auto=format&fit=crop&w=800&q=80",
                width="100%",
                height="100%",
                object_fit="cover",
            ),
            rx.box(
                rx.hstack(
                    rx.image(
                        src="https://static.vecteezy.com/system/resources/thumbnails/023/515/041/small/book-church-logo-design-icon-bible-church-logo-design-cross-and-holy-bible-logo-free-vector.jpg",
                        width="10%",
                        height="10%",
                        border_radius="50%",
                        border="3px solid white",
                        object_fit="cover",
                        box_shadow="0 4px 20px rgba(0,0,0,0.25)"
                    ),
                    rx.vstack(
                        rx.text(
                            church_states.ChurchState.get_church_name,
                            color="white",
                            font_weight="bold",
                            font_size="2.0em",
                        ),
                        rx.hstack(
                            rx.icon("map-pin", size=28, color="gray"),
                            rx.text(
                                f"{contact_states.ContactState.city} {contact_states.ContactState.address_line}, {contact_states.ContactState.country}",
                                color="gray",
                                font_size="1.3em",
                            ),
                        )
                    ),
                    spacing="5",
                    align="center",
                    padding_bottom="2em",
                    padding_left="1em",

                ),
                position="absolute",
                bottom="0",
                width="100%",
                padding="1em",
                background="linear-gradient(to top, rgba(0,0,0,0.7), transparent)",
            ),
            
            position="relative",
            height="220px",
            width="100%",
        ),
        no_padding=True,
    )

def stats_section():
    return section_card(
        "Statistics",
        rx.hstack(
            rx.box(
                stat_group(
                    "Church Administration",
                    stat_item("Admin", membership_states.MembershipState.role_counts.get('church_admin'), icon_text="shield-check", icon_color="#6366F1"),
                    stat_item("Pastor", membership_states.MembershipState.role_counts.get('pastor', 0), icon_text="user-star", icon_color="#6366F1"),
                    stat_item("Deacon", membership_states.MembershipState.role_counts.get('deacon', 0), icon_text="user-check", icon_color="#6366F1"),
                    stat_item("Teacher", membership_states.MembershipState.role_counts.get('teacher', 0), icon_text="book-open", icon_color="#6366F1"),
                    stat_item("Counselor", membership_states.MembershipState.role_counts.get('counselor', 0), icon_text="hand-helping", icon_color="#6366F1"),
                    stat_item("Member", membership_states.MembershipState.role_counts.get('member', 0), icon_text="user", icon_color="#6366F1"),
                    stat_item("Payer Members", membership_states.MembershipState.role_counts.get('prayer_team', 0), icon_text="heart_handshake", icon_color="#6366F1"),
                    columns="3",
                    icon_text="crown",
                    icon_color="#6366F1",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Member Categories",
                    stat_item("Youth", membership_states.MembershipState.category_counts.get('youth', 0), icon_text="user-minus", icon_color="#057D1B"),
                    stat_item("Adult", membership_states.MembershipState.category_counts.get('adult', 0), icon_text="user", icon_color="#057D1B"),
                    stat_item("Elder", membership_states.MembershipState.role_counts.get('elder', 0), icon_text="user-plus", icon_color="#057D1B"),
                    columns="2",
                    icon_text="users",
                    icon_color="#057D1B",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Prayer Request",
                    stat_item("Prayed", "0", icon_text="circle-check", icon_color="#057D1B"),
                    stat_item("Pending", "0", icon_text="clock", icon_color="#D97706"),
                    stat_item("Rejected", "0", icon_text="circle-x", icon_color="#D90606"),
                    columns="2",
                    icon_text="heart-handshake",
                    icon_color="#D97706",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Church Activities",
                    stat_item("Marriages", "0", icon_text="heart", icon_color="#F163D9"),
                    stat_item("Child Dedication", "0", icon_text="baby", icon_color="#F163D9"),
                    stat_item("Testimonies", "0", icon_text="message-circle-more", icon_color="#F163D9"),
                    columns="2",
                    icon_text="calendar",
                    icon_color="#F163D9",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),

            spacing="5",
            width="100%",
        ),
        icon_text="chart-no-axes-column",
        icon_color="#6366F1",
    )

def contact_section():
    return section_card(
        "Contact Information",
            rx.hstack(
                rx.box(
                    stat_group(
                        "Address",
                        list_item(f"{contact_states.ContactState.city} {contact_states.ContactState.address_line}, {contact_states.ContactState.country}", icon_text="map-pin", icon_color="#6366F1"),
                        list_item(f"{contact_states.ContactState.phone_1}", icon_text="phone", icon_color="#6366F1"),
                        list_item(f"{contact_states.ContactState.phone_2}", icon_text="phone", icon_color="#6366F1"),
                        list_item(f"{contact_states.ContactState.email}", icon_text="mail", icon_color="#6366F1"),
                        list_item(f"{contact_states.ContactState.website}", icon_text="globe", icon_color="#6366F1"),
                        columns="1",
                    ),
                    padding="1em",
                    border_radius="12px",
                    background="#f9fafb",
                    width="45%",
                ),
                rx.box(
                    rx.text(
                        "Social",
                        font_size="0.9em",
                        font_weight="600",
                        margin_bottom="0.8em",
                    ),

                    rx.grid(
                        # Facebook
                        rx.link(
                            rx.center(
                                rx.image(
                                    src="/images/facebook.png",
                                    width="25px",
                                    height="25px",
                                    object_fit="contain",
                                ),

                                width="40px",
                                height="40px",
                                border="1.5px solid rgba(0,0,0,0.12)",
                                background="rgba(255,255,255,0.6)",
                                border_radius="14px",
                                transition="all 0.2s ease",
                                _hover={
                                    "transform": "scale(1.05)",
                                    "background": "white",
                                },
                            ),

                            href=contact_states.ContactState.facebook,
                            is_external=True,
                        ),

                        # YouTube
                        rx.link(
                            rx.center(
                                rx.image(
                                    src="/images/youtube.png",
                                    width="25px",
                                    height="25px",
                                    object_fit="contain",
                                ),

                                width="40px",
                                height="40px",
                                border="1.5px solid rgba(0,0,0,0.12)",
                                background="rgba(255,255,255,0.6)",
                                border_radius="14px",
                                transition="all 0.2s ease",
                                _hover={
                                    "transform": "scale(1.05)",
                                    "background": "white",
                                },
                            ),

                            href=contact_states.ContactState.youtube,
                            is_external=True,
                        ),

                        # Instagram
                        rx.link(
                            rx.center(
                                rx.image(
                                    src="/images/instagram.png",
                                    width="25px",
                                    height="25px",
                                    object_fit="contain",
                                ),

                                width="40px",
                                height="40px",
                                border="1.5px solid rgba(0,0,0,0.12)",
                                background="rgba(255,255,255,0.6)",
                                border_radius="14px",
                                transition="all 0.2s ease",
                                _hover={
                                    "transform": "scale(1.05)",
                                    "background": "white",
                                },
                            ),

                            href=contact_states.ContactState.instagram,
                            is_external=True,
                        ),

                        columns="5",
                        spacing="4",
                        justify="center",
                    ),

                    padding="1.2em",
                    border_radius="16px",
                    background="#f9fafb",
                    width="55%",
                ),
                spacing="5",
                width="100%",
            ),
        action=edit_button(contact_states.ContactFormState.open_modal),
        icon_text="phone",
        icon_color="#6366F1",
    )

# THEME
def theme_section():
    return section_card(
        "Theme",
        rx.box(
            rx.hstack(
                # Left icon container
                rx.center(
                    rx.icon(
                        "sparkles",
                        size=28,
                        color="#BE9DF7",
                    ),

                    width="60px",
                    height="60px",
                    border_radius="16px",
                    background="rgba(124,58,237,0.12)",
                    border="1px solid rgba(124,58,237,0.18)",
                    flex_shrink="0",
                ),

                # Theme text
                rx.vstack(
                    rx.text(
                        theme_states.ThemeState.theme,
                        font_size="1.35em",
                        font_weight="700",
                        color="#FFFFFF",
                        line_height="1.4",
                    ),

                    rx.text(
                        theme_states.ThemeState.verse,
                        font_size="0.95em",
                        color="#D9DADC",
                        font_style="italic",
                        line_height="1.6",
                    ),

                    align="start",
                    spacing="2",
                    width="100%",
                ),

                spacing="4",
                align="start",
                width="100%",
            ),

            padding="1.3em",
            border_radius="20px",

            # Background design
            background="""
                linear-gradient(
                    135deg,
                    #0F172A 0%,
                    #1E1B4B 30%,
                    #312E81 65%,
                    #4C1D95 100%
                )
                """,

            border="1px solid rgba(124,58,237,0.12)",
            box_shadow="0 4px 20px rgba(0,0,0,0.04)",
            width="100%",
        ),

        action=edit_button(theme_states.ThemeFormState.open_modal),
        icon_text="star",
        icon_color="#7C3AED",
    )

def church_profile_card():
    return rx.box(
        rx.flex(
            profile_section(),
            stats_section(),
            rx.hstack(
                rx.fragment(
                    contact_section(),
                    contact_modal(),
                ),
                rx.fragment(
                    theme_section(),
                    theme_modal(),
                ),
                spacing="4",
                width="100%",
            ),
            wrap="wrap",
            spacing="6",
        ),
        padding="1em",
        padding_top="3em",
        background="#f5f7fb",
        min_height="100vh",
    )

# MODALS
def labeled_input(label, placeholder, state, state_func=None):
    return rx.vstack(
        rx.text(label, font_size="0.9em", font_weight="500"),
        rx.input(placeholder=placeholder, value=state, on_change=state_func),
        align="start",
        spacing="1",
        width="100%",
    )

def labeled_textarea(label, placeholder, state, state_func=None, focus=False):
    return rx.vstack(
        rx.text(label, font_size="0.9em", font_weight="500"),
        rx.text_area(placeholder=placeholder, value=state, on_change=state_func, auto_focus=focus),
        align="start",
        spacing="1",
        width="100%",
    )

def contact_modal():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Contact"),
            rx.text(contact_states.ContactFormState.error, color='red'),
            rx.vstack(
                labeled_input("Country", "Enter country", contact_states.ContactFormState.country, contact_states.ContactFormState.set_country),
                labeled_input("City", "Enter city", contact_states.ContactFormState.city, contact_states.ContactFormState.set_city),
                labeled_input("Address", "Enter address", contact_states.ContactFormState.address_line, contact_states.ContactFormState.set_address_line),
                labeled_input("Email", "Enter email", contact_states.ContactFormState.email, contact_states.ContactFormState.set_email),
                labeled_input("Phone 1", "Enter phone number 1", contact_states.ContactFormState.phone_1, contact_states.ContactFormState.set_phone_1),
                labeled_input("Phone 2", "Enter phone number 2", contact_states.ContactFormState.phone_2, contact_states.ContactFormState.set_phone_2),

                rx.divider(margin_y="1em"),

                # SOCIALS SECTION
                rx.vstack(
                    rx.text(
                        "Social Media & Website",
                        font_size="1em",
                        font_weight="600",
                    ),
                    rx.text(
                        "Add your church online presence links",
                        font_size="0.8em",
                        color="gray",
                    ),

                    rx.hstack(
                        rx.input(placeholder="YouTube", value=contact_states.ContactFormState.youtube, on_change=contact_states.ContactFormState.set_youtube),
                        rx.input(placeholder="Facebook", value=contact_states.ContactFormState.facebook, on_change=contact_states.ContactFormState.set_facebook),
                        spacing="3",
                        width="100%",
                    ),

                    rx.hstack(
                        rx.input(placeholder="Instagram", value=contact_states.ContactFormState.instagram, on_change=contact_states.ContactFormState.set_instagram),
                        rx.input(placeholder="Website", value=contact_states.ContactFormState.website, on_change=contact_states.ContactFormState.set_website),
                        spacing="3",
                        width="100%",
                    ),

                    align="start",
                    width="100%",
                    spacing="2",
                ),

                # ACTION BUTTONS
                rx.hstack(
                    rx.button("Cancel", variant="soft",  on_click=contact_states.ContactFormState.close_modal),
                    rx.button("Save Changes", color_scheme="green", on_click=contact_states.ContactFormState.save_contact),
                    justify="end",
                    width="100%",
                    margin_top="1em",
                ),

                spacing="4",
                width="100%",
            ),
            max_width="500px",
        ),
        open=contact_states.ContactFormState.is_open,
    )

def theme_modal():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Theme"),
            rx.text(theme_states.ThemeFormState.error, color='red'),
            rx.vstack(
                labeled_input("Year", "Enter year", theme_states.ThemeFormState.year, theme_states.ThemeFormState.set_year),
                labeled_textarea("Theme", "Enter theme", theme_states.ThemeFormState.theme, theme_states.ThemeFormState.set_theme, focus=True),
                labeled_input("Verse", "Enter (,) separated verses", theme_states.ThemeFormState.verse, theme_states.ThemeFormState.set_verse),
                # ACTION BUTTONS
                rx.hstack(
                    rx.button("Cancel", variant="soft",  on_click=theme_states.ThemeFormState.close_modal),
                    rx.button("Save Changes", color_scheme="green", on_click=theme_states.ThemeFormState.save_theme),
                    justify="end",
                    width="100%",
                    margin_top="1em",
                ),

                spacing="4",
                width="100%",
            ),
            max_width="500px",
        ),
        open=theme_states.ThemeFormState.is_open,
    )