import reflex as rx

from app.states.auth import AuthState

class DashboardState(rx.State):
    current_page: str = 'church'

    @rx.event
    def set_page(self, page: str) -> None:
        self.current_page = page
