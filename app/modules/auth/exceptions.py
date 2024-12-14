from fastapi import status
from app.core.exceptions_abstract import ErrorAbstract

class AuthenticationException(ErrorAbstract):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication error"