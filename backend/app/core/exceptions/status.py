"""Define custom exceptions for the status"""
from .base import AppException


class StatusNotFound(AppException):
    """Status not found exception
    Announcement requires a status. So, 
    Raised when the status name given doesn't correspond to a status in the database.
    """

    status_code = 404
    detail = "Status not found"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
