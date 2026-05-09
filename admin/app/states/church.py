import reflex as rx
from app.services import church as church_services

class ChurchState(rx.State):
    name: str = ""
    church: dict = {}
    churches: list[dict] = []
    contact: dict[str, str] = {}

    def set_church(self, value: str):
        self.church = value

    def set_name(self, value: str):
        self.name = value

    @rx.var
    def get_church_name(self) -> str:
        return self.church.get('name', '')
    
    @rx.event
    def load_churches(self):
        self.churches = church_services.get_churches()

    @rx.event
    def add_church(self):
        if self.name:
            church_services.create_church(self.name)
            self.name = ""
            self.load_churches()

