import reflex as rx

from app.states.announcement import AnnouncementListState, AnnouncementTagState
from app.states.status import StatusState
from app.states.audience import AudienceState
from app.states.church import ChurchState
from app.states.invite import InviteFormState, InvitetListState

class DashboardState(rx.State):
    current_page: str = 'church'
    church_name: str
    church: dict = {}
    
    @rx.event
    async def set_page(self, page: str) -> None:
        if page == 'announcements':
            tag_state = await self.get_state(AnnouncementTagState)
            await tag_state.get_tags()

            status_state = await self.get_state(StatusState)
            await status_state.get_active_status()

            audience_state = await self.get_state(AudienceState)
            await audience_state.get_active_audiences()

            announcement_list_state = await self.get_state(AnnouncementListState)
            await announcement_list_state.paginated_announcements()

        if page == 'invites':
            church_state = await self.get_state(ChurchState)

            invite_form_state = await self.get_state(InviteFormState)
            invite_form_state.church_code = church_state.church['code']

            invite_list_state = await self.get_state(InvitetListState)
            await invite_list_state.paginated_invites()
        self.current_page = page

    @rx.var
    def get_church_name(self) -> str:
        return self.church.get('name', '')

