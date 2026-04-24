import reflex as rx

from app.pages.header import dashboard_header
from app.pages.sidebar import dashboard_sidebar
from app.pages.content import dashboard_content

def dashboard_page():
    return rx.vstack(
        dashboard_header(),

        rx.hstack(
            dashboard_sidebar(),
            dashboard_content(),
            position="absolute",
            top="80px",
            left="0",
            right="0",
            bottom="0",
        ),
        height="100vh",
        overflow="hidden",
    )