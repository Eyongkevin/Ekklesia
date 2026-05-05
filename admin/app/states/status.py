import reflex as rx

from app.services import status as status_service

class StatusState(rx.State):
    statuses: list[dict[str, str | bool]]

    def get_active_status(self):
        self.statuses = status_service.get_active_status()

    @rx.var
    def get_status_names(self) -> list[str]:
        return [status.get('name') for status in self.statuses]
