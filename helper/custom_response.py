from rest_framework import status
from rest_framework.response import Response
from helper import status_codes
from helper.errors import Error


class CustomResponse:
    data = {}
    error = {}
    success = ""
    last_page = 0
    error_code = status_codes.NO_ERROR

    def __init__(self, success=True, data=None, error: dict = None, error_code=status_codes.NO_ERROR, last_page=0):
        self.data = data
        self.error = error
        self.error_code = error_code
        self.success = success
        self.last_page = last_page

    @property
    def get_response(self):
        if self.last_page == 0:
            return {
                'success': self.success,
                'error_code': self.error_code,
                'error': self.error,
                'data': self.data
            }
        else:
            return {
                'success': self.success,
                'error_code': self.error_code,
                'error': self.error,
                'data': self.data,
                'last_page': self.last_page
            }


def success_response(data: dict):
    return CustomResponse(success=True, data=data)


def missing_field_error_response(error: dict):
    return CustomResponse(success=False, error=error, error_code=status_codes.FIELDS_MISSING_OR_INVALID)


def authentication_error_response(error: dict):
    return CustomResponse(success=False, error=error, error_code=status_codes.NOT_AUTHENTICATED)
