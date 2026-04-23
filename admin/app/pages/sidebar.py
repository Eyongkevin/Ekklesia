import reflex as rx

from app.states.dashboard import DashboardState

def dashboard_sidebar():
    DashboardState.set_church_name
    return rx.vstack(
        rx.heading("Menu", size="3"),

        sidebar_item(DashboardState.get_church_name, "home", "church"),
        sidebar_item("Event & Schedule", "calendar", "events"),
        sidebar_item("Announcements", "megaphone", "announcements"),
        sidebar_item("Daily Devotion", "book", "devotion"),
        sidebar_item("Projects", "briefcase", "projects"),
        sidebar_item("Q&A", "help-circle", "qa"),

        rx.divider(),

        rx.text("Member Request", weight="bold"),

        sidebar_item("Prayer Request", "heart", "prayer"),
        sidebar_item("Marriage", "users", "marriage"),
        sidebar_item("Testimony", "star", "testimony"),
        sidebar_item("Child Dedication", "baby", "child"),
        sidebar_item("Funeral", "cross", "funeral"),

        width="250px",
        height="100%",
        overflow_y="auto",   # 👈 enables sidebar scroll
        border_right="1px solid #eee",
        padding="1em",
        align="start",

        # width="250px",
        # padding="1em",
        # border_right="1px solid #eee",
        # height="100vh",
        # overflow_y="auto",
        # position="sticky",
        # top="0",
        # align="start"
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