import reflex as rx
class DashboardState(rx.State):
    current_page: str = 'church'
    church_name: str
    church: dict = {}
    
    @rx.event
    def set_page(self, page: str) -> None:
        self.current_page = page

    @rx.var
    def get_church_name(self) -> str:
        return self.church.get('name', '')

