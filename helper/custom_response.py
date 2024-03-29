from rest_framework import status
from rest_framework.response import Response
from helper import status_codes
from helper.errors import Error


class CustomResponse:
    data = {}
    error = {}
    success = False
    error_message: str = None
    last_page = 0
    error_code = status_codes.NO_ERROR
    msg: str = None

    def __init__(self, success=True, data=None, error: dict = None, msg: str = None, error_code=status_codes.NO_ERROR,
                 error_message: str = None,
                 last_page=0):
        self.data = data
        self.error = error
        self.error_code = error_code
        self.error_message = error_message
        self.success = success
        self.msg = msg
        self.last_page = last_page

    @property
    def get_response(self):
        if self.last_page == 0:
            return {
                'success': self.success,
                'error_code': self.error_code,
                'error': self.error,
                'error_message': self.error_message,
                'data': self.data,
                'msg': self.msg
            }
        else:
            return {
                'success': self.success,
                'error_code': self.error_code,
                'error': self.error,
                'error_message': self.error_message,
                'data': self.data,
                'last_page': self.last_page,
                'msg': self.msg
            }


def success_response(data: dict = None, msg="Success"):
    return CustomResponse(success=True, data=data, msg=msg)


def missing_field_error_response(error: dict,error_message="Field Missing"):
    return CustomResponse(success=False, error=error, error_code=status_codes.FIELDS_MISSING_OR_INVALID,error_message=error_message)


def authentication_error_response(error: dict,error_message="Authentication Error"):
    return CustomResponse(success=False, error=error, error_code=status_codes.NOT_AUTHENTICATED,error_message=error_message)
