import reflex as rx

from app.states import (
    theme as theme_states,
    membership as membership_states,
    church as church_states,
    contact as contact_states
)



def stat_item(label: str, value: str):
    return rx.vstack(
        rx.text(value, font_size="1.3em", font_weight="bold"),
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
                    church_states.ChurchState.get_church_name,
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
                    stat_item("Admin", membership_states.MembershipState.role_counts.get('church_admin')),
                    stat_item("Pastor", membership_states.MembershipState.role_counts.get('pastor', 0)),
                    stat_item("Deacon", membership_states.MembershipState.role_counts.get('deacon', 0)),
                    stat_item("Teacher", membership_states.MembershipState.role_counts.get('teacher', 0)),
                    stat_item("Counselor", membership_states.MembershipState.role_counts.get('counselor', 0)),
                    stat_item("Member", membership_states.MembershipState.role_counts.get('member', 0)),
                    stat_item("Payer Members", membership_states.MembershipState.role_counts.get('prayer_team', 0)),
                    columns="3",
                ),
                padding="1em",
                border_radius="12px",
                background="#f9fafb",
            ),
            rx.box(
                stat_group(
                    "Categories",
                    stat_item("Youth", membership_states.MembershipState.category_counts.get('youth', 0)),
                    stat_item("Adult", membership_states.MembershipState.category_counts.get('adult', 0)),
                    stat_item("Elder", membership_states.MembershipState.role_counts.get('elder', 0)),
                    # stat_item("Children", "129"),
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

            spacing="5",
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
                        rx.text(contact_states.ContactState.country),
                        rx.text(f"📍 {contact_states.ContactState.city} {contact_states.ContactState.address_line}"),
                        rx.text(f"📞 {contact_states.ContactState.phone_1}"),
                        rx.text(f"📞 {contact_states.ContactState.phone_2}"),
                        rx.text(f"✉️ {contact_states.ContactState.email}"),
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
                            href=contact_states.ContactState.facebook,
                            is_external=True
                        ),
                        rx.link(
                            "YouTube",
                            rx.text(contact_states.ContactState.youtube),
                            is_external=True
                        ),
                        rx.link(
                            "Instagram",
                            rx.text(contact_states.ContactState.instagram),
                            is_external=True
                        ),
                        rx.link(
                            "Website",
                            rx.text(contact_states.ContactState.website),
                            is_external=True
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
        action=edit_button(contact_states.ContactFormState.open_modal),
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