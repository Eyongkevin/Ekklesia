import reflex as rx
from app.services import membership as membership_service

class MembershipState(rx.State):
    role_counts: dict[str, int] = {
        "church_admin": 0,
        "member": 0,
        "prayer_team": 0,
        "pastor": 0,
        "deacon": 0,
        "teacher": 0,
        "counselor": 0
    }

    category_counts: dict[str, int] = {
        "youth": 0,
        "adult": 0,
        "elder": 0,
        # "CHILDREN": 0,
    }
    new_members_7d: int = 0

    @rx.event
    def set_stats(self, church_id: str) -> None:
        data = membership_service.get_membership_stats(church_id)
        self.role_counts = data.get('role_counts', {})
        self.category_counts = data.get('category_counts', {})