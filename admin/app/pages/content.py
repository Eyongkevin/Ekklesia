import reflex as rx

from app.states.dashboard import DashboardState

def dashboard_content():
    pages = {
        "church": rx.text("Church Overview Page"),
        "events": rx.text("Events Page"),
        "announcements": rx.text("Announcements Page"),
        "devotion": rx.text("Daily Devotion Page"),
        "projects": rx.text("Projects Page"),
        "qa": rx.text("Q&A Page"),
        "prayer": rx.text("Prayer Requests"),
        "marriage": rx.text("Marriage Requests"),
        "testimony": rx.text("Testimonies"),
        "child": rx.text("Child Dedication"),
        "funeral": rx.text("Funeral Requests"),
    }

    return rx.box(
        pages.get(
            DashboardState.current_page,
            rx.text("Page not found")
        ),
        height="100%",
        width="100%",
        overflow_y="auto",   # 👈 independent scroll
        padding="2em",
        # width="100%",
        # # flex="1",
        # overflow_y="auto",
        # padding="2em",
    )
