from typing import Optional, TypedDict, List
from datetime import date
import reflex as rx

from app.services import announcement as announcement_service
from app.states.status import StatusState
from app.states.church import ChurchState

class AnnouncementType(TypedDict):
    id: int
    title: str
    content: str
    status: dict[str, str | bool]
    publish_at: Optional[str]
    expire_at: Optional[str]
    created_by: str
    is_pinned: bool
    links: list[dict[str, str]]
    tags: List[dict[str, str | bool]]
    audiences: List[dict[str, str | bool]]
    created_at: str
    modified_at: str

sample_announcements: list[AnnouncementType] = [
    {
        "id": 1,
        "title": "Baptism Service - May Edition",
        "content": "Join us this Sunday for the baptism of new members after the main service.",
        "status": "Published",
        "published_at": "2026-05-01 18:00",
        "tags": ['Prayer', 'Event', 'Conference'],
        "audience": ['Men'], 
    },
    {
        "id": 2,
        "title": "Youth Conference 2026",
        "content": "A powerful gathering for young people with guest speakers and worship sessions.",
        "status": "Scheduled",
        "published_at": "2026-05-10 10:00",
        "tags": ["Conference"],
        "audience": ["Youth"],
    },
    {
        "id": 3,
        "title": "Weekly Prayer Meeting",
        "content": "Join us every Wednesday evening for a time of prayer and intercession.",
        "status": "Published",
        "published_at": "2026-04-28 17:30",
        "tags": ['Prayer', 'General', 'Urgent'],
        "audience": ['All Members'],
    },
    {
        "id": 4,
        "title": "Church Cleanup Exercise",
        "content": "Volunteers are needed this Saturday to help clean and organize the church premises.",
        "status": "Draft",
        "published_at": "",
        "tags": ["Baptism", "Urgent"],
        "audience": ["Youth"],
    },
    {
        "id": 5,
        "title": "Marriage Seminar",
        "content": "A seminar focused on building strong and lasting relationships.",
        "status": "Expired",
        "published_at": "2026-03-15 09:00",
        "tags": ["Baptism", "Urgent"],
        "audience": ["Members", "Leaders"],
    },
    {
        "id": 6,
        "title": "Choir Auditions",
        "content": "Interested in joining the choir? Auditions will be held this Friday.",
        "status": "Published",
        "published_at": "2026-04-30 16:00",
        "tags": [],
        "audience": [],
    },
    {
        "id": 7,
        "title": "Leadership Training",
        "content": "Training session for all department leaders and assistants.",
        "status": "Scheduled",
        "published_at": "2026-05-12 14:00",
        "tags": [],
        "audience": [],
    },
    {
        "id": 8,
        "title": "Easter Thanksgiving Service",
        "content": "A special thanksgiving service celebrating the resurrection of Christ.",
        "status": "Expired",
        "published_at": "2026-04-05 08:00",
        "tags": [],
        "audience": [],
    },
    {
        "id": 9,
        "title": "New Members Orientation",
        "content": "Orientation session to welcome and guide new members of the church.",
        "status": "Published",
        "published_at": "2026-05-02 11:00",
        "tags": [],
        "audience": [],
    },
    {
        "id": 10,
        "title": "Evangelism Outreach",
        "content": "Join the outreach team as we spread the gospel in nearby communities.",
        "status": "Draft",
        "published_at": "",
        "tags": [],
        "audience": [],
    },
]

class AnnouncementState(rx.State):
    show_add_update_drawer: bool = False

    @rx.event
    async def open_add_update_drawer(self):
        status_state = await self.get_state(StatusState)
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
        from app.states.auth import AuthState

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

    def set_new_link_title(self, value: str):
        self.new_link_title = value
    
    def set_new_link(self, value: str):
        self.new_link = value

    def set_content(self, value: str):
        self.content = value
    
    def set_title(self, value: str):
        self.title = value

    def set_status(self, value: str):
        self.status = value

    def set_pin_to_top(self, value: bool):
        self.pin_to_top = value

    def set_publish_date(self, value: str):
        self.publish_date = value

    def set_expire_date(self, value: str):
        self.expire_date = value


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

class AnnouncementTagState(rx.State):
    name: str
    description: str
    tags: list[dict[str, str | bool]]

    def get_tags(self):
        self.tags = announcement_service.get_tags()

    @rx.var
    def get_tags_name(self) -> list[str]:
        return [tag.get('name') for tag in self.tags]

class AnnouncementFilterState(rx.State):
    search: str = ""
    status: str = "Published"
    audience: str = "All Members"
    tag: str = "All Tags"


    async def set_search(self, value: str):
        self.search = value
        announcement_list_state = await self.get_state(AnnouncementListState)
        await announcement_list_state.paginated_announcements()

    async def set_status(self, value: str):
        self.status = value
        announcement_list_state = await self.get_state(AnnouncementListState)
        await announcement_list_state.paginated_announcements()

    async def set_audience(self, value: str):
        self.audience = value
        announcement_list_state = await self.get_state(AnnouncementListState)
        await announcement_list_state.paginated_announcements()

    async def set_tag(self, value: str):
        self.tag = value
        announcement_list_state = await self.get_state(AnnouncementListState)
        await announcement_list_state.paginated_announcements()

    def set_start_date(self, value: str):
        self.start_date = value

    def set_end_date(self, value: str):
        self.end_date = value

class AnnouncementListState(rx.State):
    announcements: list[AnnouncementType] = []  # fetched from backend

    page: int = 1
    per_page: int = 3
    total_pages: int = 1

    selected_ids: set[int] = set()

    open_menu_id: int | None = None

    def toggle_menu(self, announcement_id: int):
        if self.open_menu_id == announcement_id:
            self.open_menu_id = None
        else:
            self.open_menu_id = announcement_id

    async def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            await self.paginated_announcements()

    async def prev_page(self):
        if self.page > 1:
            self.page -= 1
            await self.paginated_announcements()

    def toggle_select(self, announcement_id: int):
        if announcement_id in self.selected_ids:
            self.selected_ids.remove(announcement_id)
        else:
            self.selected_ids.add(announcement_id)

    def select_all(self):
        current_ids = [a["id"] for a in self.announcements]
        self.selected_ids = set(current_ids)

    def clear_selection(self):
        self.selected_ids = set()

    async def paginated_announcements(self)-> None:
        # start = (self.page - 1) * self.per_page
        # end = start + self.per_page
        church_state: ChurchState = await self.get_state(ChurchState)
        church_id = church_state.church.get('id')

        filter_state = await self.get_state(AnnouncementFilterState)

        announcements = announcement_service.get_announcements(
            church_id=church_id,
            status=filter_state.status,
            audience=filter_state.audience,
            tag=filter_state.tag,
            search=filter_state.search,
            is_active=True,
            page=self.page,
            per_page=self.per_page
        )
        self.total_pages = announcements.get("total", 0) // self.per_page + 1
        self.announcements = announcements.get("announcements", [])

    # @rx.var
    # def total_pages(self) -> int:
    #     return (len(self.announcements) + self.per_page - 1) // self.per_page