from typing import Callable

import reflex as rx

from app.services import auth as auth_service
from app.services import church as church_service
from app.states.dashboard import DashboardState
from app.states.contact import ContactState


class AuthState(rx.State):
    user: dict = {}
    is_authenticated: bool = False
    error: str = ""

    @rx.event
    async def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")
        
        dashboard_state: DashboardState = await self.get_state(DashboardState)
        dashboard_state.church = church_service.get_church_by_user(self.user.get('id', ''))

        church_contact_state: ContactState = await self.get_state(ContactState)
        church_contact_state.set_church_contact(dashboard_state.church.get('id'))

    def set_auth(self, user: dict):
        self.user = user
        self.is_authenticated = True

    @rx.event
    def logout(self):
        self.token = ""
        self.user = {}
        self.is_authenticated = False
        return rx.redirect("/login")
    

class LoginState(AuthState):
    email: str = ""
    password: str = ""

    @rx.event
    def set_email(self, value: str) -> None:
        self.email = value

    @rx.event
    def set_password(self, value: str) -> None:
        self.password = value
    
    @rx.event
    async def login(self) -> None:
        try:
            success = await auth_service.login(self.email, self.password)
            self.set_auth(success['user'])

            return rx.redirect('/dashboard')

        except Exception as e:
            self.set_password('')
            if hasattr(e, "response") and e.response is not None:
                data = e.response.json()
                self.error = data.get("detail", "Login failed")
            else:
                self.error = "Network error"
