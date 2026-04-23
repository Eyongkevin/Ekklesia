import reflex as rx

from app.states.contact import ContactState, ContactFormState
from app.states import theme as theme_states


def stat_item(label: str, value: str):
    return rx.vstack(
        rx.text(value, font_size="1.5em", font_weight="bold"),
        rx.text(label, font_size="0.9em", color="gray"),
        align="center",
        padding="0.1em"
    )

def section_card(title: str, content, no_padding: bool = False, action=None):
    return rx.box(
        rx.vstack(
            rx.hstack(
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

def stat_group(title: str, *items, columns="3"):
    return rx.vstack(
        rx.text(
            title,
            font_weight="bold",
            color="gray",
            font_size="0.9em",
        ),
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
                rx.text(
                    "Grace Community Church",
                    color="white",
                    font_weight="bold",
                    font_size="1.2em",
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
                    "Roles",
                    stat_item("Admin", "2"),
                    stat_item("Pastor", "2"),
                    stat_item("Deacon", "2"),
                    stat_item("Teacher", "10"),
                    stat_item("Counselor", "7"),
                    stat_item("Member", "752"),
                    columns="3",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Categories",
                    stat_item("Youth", "327"),
                    stat_item("Adult", "215"),
                    stat_item("Elder", "81"),
                    stat_item("Children", "129"),
                    columns="2",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Prayer Request",
                    stat_item("Prayed", "45"),
                    stat_item("Pending", "12"),
                    stat_item("Rejected", "3"),
                    columns="2",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Church Activities",
                    stat_item("Marriages", "12"),
                    stat_item("Child Dedication", "8"),
                    stat_item("Testimonies", "21"),
                    columns="2",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),

            spacing="9",
            width="100%",
        ),
    )

def contact_section():
    return section_card(
        "Contact",
            rx.vstack(
                rx.box(
                    stat_group(
                        "Address",
                        rx.text(ContactState.country),
                        rx.text(f"📍 {ContactState.city} {ContactState.address_line}"),
                        rx.text(f"📞 {ContactState.phone_1}"),
                        rx.text(f"📞 {ContactState.phone_2}"),
                        rx.text(f"✉️ {ContactState.email}"),
                        columns="1",
                    ),
                    padding="1em",
                    border_radius="12px",
                    background="#f9fafb",
                ),
                rx.box(
                    stat_group(
                        "Social",
                        rx.link(
                            "Facebook",
                            href=ContactState.facebook
                        ),
                        rx.link(
                            "YouTube",
                            rx.text(ContactState.youtube),
                        ),
                        rx.link(
                            "Instagram",
                            rx.text(ContactState.instagram),
                        ),
                        rx.link(
                            "Website",
                            rx.text(ContactState.website),
                        ),
                        columns="1",
                    ),
                    padding="1em",
                    border_radius="12px",
                    background="#f9fafb",
                ),

            spacing="5",
            width="100%",
            ),
        action=edit_button(ContactFormState.open_modal),
    )

# THEME
def theme_section():
    return section_card(
        "Theme",
        rx.box(
            rx.vstack(
                rx.text(
                    theme_states.ThemeState.theme,
                    font_size="1.4em",
                    font_weight="600",
                    line_height="1.4",
                ),

                rx.text(
                    f"{theme_states.ThemeState.verse}",
                    font_size="0.9em",
                    color="gray",
                    font_style="italic",
                ),

                align="start",
                spacing="2",
            ),
            border_left="4px solid #6366F1",
            padding_left="1em",
            width="100%",
        ),
        action=edit_button(theme_states.ThemeFormState.open_modal)
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
                width="50%",
            ),
            wrap="wrap",
            spacing="6",
        ),
        padding="2em",
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
            rx.text(ContactFormState.error, color='red'),
            rx.vstack(
            # COUNTRY
            labeled_input("Country", "Enter country", ContactFormState.country, ContactFormState.set_country),
            # CITY
            labeled_input("City", "Enter city", ContactFormState.city, ContactFormState.set_city),
            # ADDRESS
            labeled_input("Address", "Enter address", ContactFormState.address_line, ContactFormState.set_address_line),
            # EMAIL
            labeled_input("Email", "Enter email", ContactFormState.email, ContactFormState.set_email),
            # PHONE 1
            labeled_input("Phone 1", "Enter phone number 1", ContactFormState.phone_1, ContactFormState.set_phone_1),
            # PHONE 2
            labeled_input("Phone 2", "Enter phone number 2", ContactFormState.phone_2, ContactFormState.set_phone_2),

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
                    rx.input(placeholder="YouTube", value=ContactFormState.youtube, on_change=ContactFormState.set_youtube),
                    rx.input(placeholder="Facebook", value=ContactFormState.facebook, on_change=ContactFormState.set_facebook),
                    spacing="3",
                    width="100%",
                ),

                rx.hstack(
                    rx.input(placeholder="Instagram", value=ContactFormState.instagram, on_change=ContactFormState.set_instagram),
                    rx.input(placeholder="Website", value=ContactFormState.website, on_change=ContactFormState.set_website),
                    spacing="3",
                    width="100%",
                ),

                align="start",
                width="100%",
                spacing="2",
            ),

            # ACTION BUTTONS
            rx.hstack(
                rx.button("Cancel", variant="soft",  on_click=ContactFormState.close_modal),
                rx.button("Save Changes", color_scheme="green", on_click=ContactFormState.save_contact),
                justify="end",
                width="100%",
                margin_top="1em",
            ),

            spacing="4",
            width="100%",
        ),
        max_width="500px",

        ),
        open=ContactFormState.is_open,
    )

def theme_modal():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Theme"),
            rx.text(theme_states.ThemeFormState.error, color='red'),
            rx.vstack(
            # YEAR
            labeled_input("Year", "Enter year", theme_states.ThemeFormState.year, theme_states.ThemeFormState.set_year),
            # THEME
            labeled_textarea("Theme", "Enter theme", theme_states.ThemeFormState.theme, theme_states.ThemeFormState.set_theme, focus=True),
            # VERSE
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