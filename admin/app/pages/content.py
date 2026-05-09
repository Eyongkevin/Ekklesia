import reflex as rx

from app.states.dashboard import DashboardState
from app.pages.contents import profile, announcement

def dashboard_content():
    return rx.box(
        rx.match(
            DashboardState.current_page,
            ("church", profile.church_profile_card()),
            ("events", rx.text("Events Page")),
            ("announcements", announcement.church_announcement_card()),
            ("devotion", rx.text("Daily Devotion Page")),
            ("projects", rx.text("Projects Page")),
            ("qa", rx.text("Q&A Page")),
            ("prayer", rx.text("Prayer Requests")),
            ("marriage", rx.text("Marriage Requests")),
            ("testimony", rx.text("Testimonies")),
            ("child", rx.text("Child Dedication")),
            ("funeral", rx.text("Funeral Requests")),
            rx.text("Page not found")
        ),
        height="100%",
        width="100%",
        overflow_y="auto",
        padding="1em",
    )
