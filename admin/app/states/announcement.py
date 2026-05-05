from typing import Optional
from datetime import date
import reflex as rx

from app.services import announcement as announcement_service
from app.states.status import StatusState
from app.states.audience import AudienceState
from app.states.auth import AuthState
from app.states.church import ChurchState


class AnnouncementState(rx.State):
    show_add_update_drawer: bool = False

    @rx.event
    async def open_add_update_drawer(self):
        tag_state = await self.get_state(AnouncementTagState)
        tag_state.get_tags()

        status_state = await self.get_state(StatusState)
        status_state.get_active_status()

        audience_state = await self.get_state(AudienceState)
        audience_state.get_active_audiences()

        announcement_form_state = await self.get_state(AnnouncementFormState)
        #? We want the default to be 'Published'. So, here it needs to be the second status
        announcement_form_state.status = status_state.get_status_names[1]
        announcement_form_state.publish_date = str(date.today())

        self.show_add_update_drawer = True

    @rx.event
    def close_add_update_drawer(self):
        self.show_add_update_drawer = False

class AnnouncementFormState(rx.State):
    title: str = ""
    max_title_len: int = 100
    status: str = "Draft"
    pin_to_top: bool = True
    tags: list[str] = []
    audiences: list[str] = []
    publish_date: Optional[str] = None
    expire_date: Optional[str] = None
    content: str = ""

    # links
    links: list[dict[str, str]] = []
    max_links: int = 3
    show_link_popup: bool = False
    new_link: str = ""
    new_link_title: str = ""

    async def submit(self):
        auth_state: AuthState = await self.get_state(AuthState)
        created_by = auth_state.user.get('id')

        church_state: ChurchState = await self.get_state(ChurchState)
        church_id = church_state.church.get('id')

        announcement_service.submit(
            title=self.title,
            content=self.content,
            is_pinned=self.pin_to_top,
            links=self.links,
            status=self.status,
            publish_at=self.publish_date,
            expire_at=self.expire_date,
            tags=self.tags,
            audiences=self.audiences,
            created_by=created_by,
            church_id=church_id
        )

        self.reset_form()


    def toggle_link_popup(self):
        self.show_link_popup = not self.show_link_popup

    def add_link(self):
        if  self.new_link and self.new_link_title and not self.is_max_links_reached:
            self.links.append({
                'title': self.new_link_title,
                'url': self.new_link
            })
        self.new_link = ""
        self.show_link_popup = False

    def remove_link(self, link: dict[str, str]):
        self.links.remove(link)

    def toggle_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            self.tags.append(tag)

    def toggle_audience(self, audience: str):
        if audience in self.audiences:
            self.audiences.remove(audience)
        else:
            self.audiences.append(audience)

    @rx.var
    def is_max_links_reached(self) -> bool:
        return len(self.links) >= self.max_links 

    @rx.var
    def get_title_len(self) -> int:
        return len(self.title)
    
    @rx.var
    def toggle_submit_disable(self) -> bool:
        return len(self.title) < 2

    @rx.event
    def reset_form(self):
        self.reset()

    @rx.event
    def set_title(self, title: str):
        self.title = title[:self.max_title_len]

    @rx.event
    def set_status(self, status: str):
        self.status = status
        if self.status == 'Draft' or self.status == "Scheduled":
            self.publish_date = ""
        elif self.status == 'Published':
            self.publish_date = str(date.today())

class AnouncementTagState(rx.State):
    name: str
    description: str
    tags: list[dict[str, str | bool]]

    def get_tags(self):
        self.tags = announcement_service.get_tags()

    @rx.var
    def get_tags_name(self) -> list[str]:
        return [tag.get('name') for tag in self.tags]


