"""Define custom exceptions for announcement"""
from .base import AppException


class AnnouncementNotFound(AppException):
    """Announcement not found exception"""

    status_code = 404
    detail = "Announcement not found"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
