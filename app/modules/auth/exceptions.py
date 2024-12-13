from http import HTTPStatus
from app.core.exceptions_abstract import ErrorAbstract

class AuthenticationException(ErrorAbstract):
    status_code = HTTPStatus.UNAUTHORIZED
    message = "Invalid username or password"