import reflex as rx

from app.states.announcement import AnnouncementListState, AnnouncementTagState
from app.states.status import StatusState
from app.states.audience import AudienceState

class DashboardState(rx.State):
    current_page: str = 'church'
    church_name: str
    church: dict = {}
    
    @rx.event
    async def set_page(self, page: str) -> None:
        if page == 'announcements':
            tag_state = await self.get_state(AnnouncementTagState)
            tag_state.get_tags()

            status_state = await self.get_state(StatusState)
            status_state.get_active_status()

            audience_state = await self.get_state(AudienceState)
            audience_state.get_active_audiences()

            announcement_list_state = await self.get_state(AnnouncementListState)
            await announcement_list_state.paginated_announcements()
        self.current_page = page

    @rx.var
    def get_church_name(self) -> str:
        return self.church.get('name', '')

