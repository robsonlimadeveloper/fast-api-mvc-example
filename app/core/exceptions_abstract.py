from wsgiref import headers
from fastapi import status
from fastapi.exceptions import HTTPException

class ErrorAbstract(HTTPException):
    '''Error abstract class'''
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = ""
    headers: dict = {}

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )

    def to_dict(self):
        '''Change message to dict'''
        exception = dict(self.headers or ())
        exception['detail'] = self.detail

        return exception
