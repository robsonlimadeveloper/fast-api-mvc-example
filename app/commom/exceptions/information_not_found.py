'''Commom Exception module'''

from app.core.exceptions_abstract import ErrorAbstract
from fastapi import status
class InformationNotFound(ErrorAbstract):
    '''Information not found'''
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Information not found."