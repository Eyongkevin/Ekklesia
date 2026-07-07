"""Define custom exceptions for the status"""
from .base import AppException


class InviteNotFound(AppException):
    """Invite not found exception

    Raised when the invite id given doesn't correspond to an invite in the database.
    """

    status_code = 404
    detail = "Invite not found"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
