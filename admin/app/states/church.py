import reflex as rx
from app.services import church as church_services

class ChurchState(rx.State):
    name: str = ""
    churches: list[dict] = []
    contact: dict[str, str] = {}

    @rx.event
    def load_churches(self):
        self.churches = church_services.get_churches()

    @rx.event
    def add_church(self):
        if self.name:
            church_services.create_church(self.name)
            self.name = ""
            self.load_churches()

