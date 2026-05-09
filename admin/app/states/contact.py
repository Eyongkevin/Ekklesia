import reflex as rx
from app.states.church import ChurchState
from app.services import church as church_service

class ContactState(rx.State):
    country: str = ""
    city: str = ""
    address_line: str = ""
    phone_1: str = ""
    phone_2: str = ""
    email: str = ""
    facebook: str = ""
    youtube: str = ""
    instagram: str = ""
    website: str = ""

    def set_church_contact(self, church_id: str):
        contact: dict[str, str] | None = church_service.get_church_contact(church_id)
        if contact:
            for key, value in contact.items():
                if hasattr(self, key) and value:
                    setattr(self, key, value)
    
class ContactFormState(rx.State):
    is_open: bool = False
    error: str = ""

    country: str = ""
    city: str = ""
    address_line: str = ""
    phone_1: str = ""
    phone_2: str = ""
    email: str = ""
    facebook: str = ""
    youtube: str = ""
    instagram: str = ""
    website: str = ""

    @rx.event
    async def open_modal(self):
        church_state = await self.get_state(ChurchState)
        church_id = church_state.church.get('id')
        self.set_church_contact(church_id)

        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    async def save_contact(self):
        church_state = await self.get_state(ChurchState)
        church_id: str = church_state.church.get('id', '')

        contact = church_service.create_church_contact(
            church_id,
            self.country,
            self.city,
            self.address_line,
            self.phone_1,
            self.phone_2,
            self.email,
            self.facebook,
            self.youtube,
            self.instagram,
            self.website
        )
        if contact:
            contact_state: ContactState = await self.get_state(ContactState)
            contact_state.set_church_contact(church_id)
            self.reset()
        else: 
            self.error = "Contact not saved. An error occured!!"

    def set_church_contact(self, church_id: str):
        contact: dict[str, str] | None = church_service.get_church_contact(church_id)
        if contact:
            for key, value in contact.items():
                if hasattr(self, key) and value:
                    setattr(self, key, value)
    
    def set_country(self, value: str):
        self.country = value

    def set_city(self, value: str):
        self.city = value

    def set_address_line(self, value: str):
        self.address_line = value   

    def set_phone_1(self, value: str):
        self.phone_1 = value

    def set_phone_2(self, value: str):
        self.phone_2 = value

    def set_email(self, value: str):
        self.email = value

    def set_facebook(self, value: str):
        self.facebook = value

    def set_youtube(self, value: str):
        self.youtube = value
    
    def set_instagram(self, value: str):
        self.instagram = value

    def set_website(self, value: str):
        self.website = value

