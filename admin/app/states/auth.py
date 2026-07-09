from typing import Optional
from datetime import date

import reflex as rx

from app.services import auth as auth_service
from app.services import church as church_service
from app.states.dashboard import DashboardState
from app.states.contact import ContactState
from app.states.theme import ThemeState
from app.states.membership import MembershipState
from app.states.church import ChurchState


class AuthState(rx.State):
    is_authenticated: bool = False
    access_token: Optional[str] = None
    error: str = ""

    @rx.event
    async def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")
        
        # Load states used in the loading of profile information.

        church_state: ChurchState = await self.get_state(ChurchState)
        church_state.church = church_service.get_church_of_user(self.access_token)
        
        church_contact_state: ContactState = await self.get_state(ContactState)
        await church_contact_state.set_church_contact(church_state.church.get('id'))

        church_theme_state: ThemeState = await self.get_state(ThemeState)
        await church_theme_state.set_church_theme(church_state.church.get('id'), date.today().year)

        membership_state: MembershipState = await self.get_state(MembershipState)
        membership_state.set_stats(church_state.church.get('id'))

    def set_auth(self, access_token: str):
        self.is_authenticated = True
        self.access_token = access_token

    @rx.event
    def logout(self):
        self.access_token = ""
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
            self.set_auth(success['access_token'])

            return rx.redirect('/dashboard')

        except Exception as e:
            self.set_password('')
            if hasattr(e, "response") and e.response is not None:
                data = e.response.json()
                self.error = data.get("detail", "Login failed")
            else:
                self.error = "Network error"
