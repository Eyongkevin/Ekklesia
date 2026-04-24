from datetime import date

import reflex as rx
from app.states.church import ChurchState
from app.services import church as church_service

class ThemeState(rx.State):
    year: int
    theme: str
    verse: str

    def set_church_theme(self, church_id: str, year: int):
        theme: dict[str, str] | None = church_service.get_church_them_by_year(church_id, year)
        if theme:
            for key, value in theme.items():
                if hasattr(self, key) and value:
                    setattr(self, key, value)
    
class ThemeFormState(rx.State):
    is_open: bool = False
    error: str = ""

    year: int
    theme: str
    verse: str

    @rx.event
    def set_year(self, year: str):
        self.year = int(year)

    @rx.event
    async def open_modal(self):
        church_state = await self.get_state(ChurchState)
        church_id: str = church_state.church.get('id', '')
        self.set_church_theme(church_id, date.today().year)

        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    async def save_theme(self):
        church_state = await self.get_state(ChurchState)
        church_id: str = church_state.church.get('id', '')

        theme = church_service.create_or_update_church_theme(
            church_id,
            self.year,
            self.theme,
            self.verse
        )
        if theme:
            theme_state: ThemeState = await self.get_state(ThemeState)
            theme_state.set_church_theme(church_id, self.year)
            self.reset()
        else: 
            self.error = "Theme not saved. An error occured!!"

    def set_church_theme(self, church_id: str, year: int):
        theme: dict[str, str] | None = church_service.get_church_them_by_year(church_id, year)
        if theme:
            for key, value in theme.items():
                if hasattr(self, key) and value:
                    setattr(self, key, value)
