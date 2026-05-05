import reflex as rx

from app.services import audience as audience_service

class AudienceState(rx.State):
    name: str
    description: str
    audiences: list[dict[str, str]]

    def get_active_audiences(self):
        self.audiences = audience_service.get_active_audience()

    @rx.var
    def get_audience_name(self) -> list[str]:
        return [audience.get('name') for audience in self.audiences]
