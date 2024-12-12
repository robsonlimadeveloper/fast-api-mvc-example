'''Commom Exception module'''

from app.core.exceptions_abstract import ErrorAbstract

class InformationNotFound(ErrorAbstract):
    '''Information not found'''
    status_code: int = 404
    message: str = "Information not found."