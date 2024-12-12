from http import HTTPStatus


class ErrorAbstract(Exception):
    '''Error abstract class'''
    status_code: int = 400
    message: str = ""

    def __init__(self, message=None, status_code=None, payload=None, server_message=""):
        super(ErrorAbstract, self).__init__()
        self.message = message or self.message
        self.server_message = server_message
        self.status_code = status_code or self.status_code
        self.payload = payload

    def to_dict(self):
        '''Change message to dict'''
        exception = dict(self.payload or ())
        exception['message'] = self.message

        return exception


class WrongParameterException(ErrorAbstract):
    '''Wrong parameter exception class'''
    status_code: int = HTTPStatus.BAD_REQUEST
    message: str = "Parameter does not exist"


class WrongValueParameterException(ErrorAbstract):
    '''Wrong value parameter exception class'''
    status_code: int = HTTPStatus.BAD_REQUEST
    message: str = "Parameter value is wrong"


class InvalidUserOrPassword(ErrorAbstract):
    '''Invalid user or password exception class'''
    message = "Invalid user or password"