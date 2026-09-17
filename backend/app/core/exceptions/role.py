"""Define custom exceptions for the role"""
from .base import AppException


class RoleNotFound(AppException):
    """role not found exception

    Raised when the role id given doesn't correspond to a role in the database.
    """

    status_code = 404
    detail = "Role not found"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail

class RoleProtectedError(AppException):
    """role is protected exception

    Raised when the role was derived from the system and is protected.
    """

    status_code = 404
    detail = "Role protected"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
