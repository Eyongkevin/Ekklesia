import reflex as rx

from app.services import status as status_service

class StatusState(rx.State):
    statuses: list[dict[str, str | bool]]

    async def get_active_status(self):
        from app.states.auth import AuthState

        auth_state: AuthState = await self.get_state(AuthState)
        self.statuses = status_service.get_active_status(auth_state.access_token)

    @rx.var
    def get_status_names(self) -> list[str]:
        return [status.get('name') for status in self.statuses]
