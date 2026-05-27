import reflex as rx

from app.states.dashboard import DashboardState
from app.states.church import ChurchState

def dashboard_sidebar():
    return rx.vstack(
        rx.heading("Menu", size="3"),

        sidebar_item(ChurchState.get_church_name, "home", "church"),
        sidebar_item("Event & Schedule", "calendar", "events"),
        sidebar_item("Announcements", "megaphone", "announcements"),
        sidebar_item("Daily Devotion", "book", "devotion"),
        sidebar_item("Projects", "briefcase", "projects"),
        sidebar_item("Q&A", "help-circle", "qa"),
        sidebar_item("Invites", "send", "invites"),

        rx.divider(),

        rx.text("Member Request", weight="bold"),

        sidebar_item("Prayer Request", "heart", "prayer"),
        sidebar_item("Marriage", "users", "marriage"),
        sidebar_item("Testimony", "star", "testimony"),
        sidebar_item("Child Dedication", "baby", "child"),
        sidebar_item("Funeral", "cross", "funeral"),

        width="250px",
        height="100%",
        overflow_y="auto",
        border_right="1px solid #eee",
        padding="1em",
        padding_top="5em",
        align="start",
    )

def sidebar_item(label: str, icon: str, page: str):
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon),
            rx.text(label),
            spacing="2",
            justify="start",
            width="100%",
        ),
        variant=rx.cond(
            DashboardState.current_page == page,
            "solid",
            "ghost"
        ),
        width="100%",
        justify="start",
        align="center",
        on_click=lambda: DashboardState.set_page(page),
    )