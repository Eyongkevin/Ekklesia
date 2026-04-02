import reflex as rx
from app.services.church import get_churches, create_church

class ChurchState(rx.State):
    name: str = ""
    churches: list[dict] = []

    @rx.event
    def load_churches(self):
        self.churches = get_churches()

    @rx.event
    def add_church(self):
        if self.name:
            create_church(self.name)
            self.name = ""
            self.load_churches()