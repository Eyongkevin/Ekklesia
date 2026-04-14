from typing import Callable

import reflex as rx

from app.services import auth as login_service


class AuthState(rx.State):
    user: dict = {}
    is_authenticated: bool = False
    error: str = ""

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

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
            success = await login_service.login(self.email, self.password)
            self.set_auth(success['user'])

            return rx.redirect('/dashboard')

        except Exception as e:
            self.set_password('')
            if hasattr(e, "response") and e.response is not None:
                data = e.response.json()
                self.error = data.get("detail", "Login failed")
            else:
                self.error = "Network error"
