import reflex as rx

from app.services import audience as audience_service

class AudienceState(rx.State):
    name: str
    description: str
    audiences: list[dict[str, str]]

    async def get_active_audiences(self):
        from app.states.auth import AuthState

        auth_state: AuthState = await self.get_state(AuthState)
        self.audiences = audience_service.get_active_audience(auth_state.access_token)

    @rx.var
    def get_audience_name(self) -> list[str]:
        return [audience.get('name') for audience in self.audiences]
