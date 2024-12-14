"""Exceptions to user data"""
from http import HTTPStatus
from app.core.exceptions_abstract import ErrorAbstract

class NameDuplicateException(ErrorAbstract):
    """Exception to name duplicate in database"""
    status_code: int = HTTPStatus.CONFLICT
    detail: str = "Invalid name. This name is already registered."

class UserNotFoundException(ErrorAbstract):
    """Exception to user not found"""
    status_code: int = HTTPStatus.NOT_FOUND
    detail: str = "User not found"

class UserNotDeleteYourselfException(ErrorAbstract):
    """Exception to user not delete yourself"""
    status_code: int = HTTPStatus.BAD_REQUEST
    detail: str = "You cannot delete yourself"