"""Exceptions to user data"""
from http import HTTPStatus
from app.core.exceptions_abstract import ErrorAbstract

class NameDuplicateException(ErrorAbstract):
    """Exception to name duplicate in database"""
    status_code: int = HTTPStatus.CONFLICT
    message: str = "Invalid name. This name is already registered."