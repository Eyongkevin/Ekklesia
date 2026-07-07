"""Define custom exceptions for the church"""
from fastapi import status
from .base import AppException


class DuplicateChurchThemeForYear(AppException):
    """Duplicate church theme for year found
    A church should have a max of one theme per year. So, 
    Raised when duplicate theme found for a church in a year.
    """

    status_code = status.HTTP_409_CONFLICT
    detail = "Duplicate church theme for the year"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail

class NoChurchCodeFound(AppException):
    """No Church code found
    A church should have a unique code. So,
    Raised when no code is found for the church
    """

    status_code = status.HTTP_404_NOT_FOUND
    detail = "No church code found"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class ChurchConstraintViolationError(AppException):
    """Church Constraint Violation Error
    Constraints needs to be respected when creating or updating a church
    """

    status_code = status.HTTP_409_CONFLICT
    detail = "Church constraint voilated"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail