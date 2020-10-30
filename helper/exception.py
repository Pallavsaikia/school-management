from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status
from helper.errors import Error
from helper import status_codes


class CustomValidation(APIException):
    status_code = status.HTTP_200_OK
    default_detail = 'A server error occurred.'
    error_code = status_codes.INTERNAL_SERVER_ERROR
    error = {}

    def __init__(self, detail=None, field=None, error: Error = None, error_msg: str = "Something went wrong",
                 error_code=status_codes.INTERNAL_SERVER_ERROR,
                 status_code=status.HTTP_200_OK):
        # if status_code is not None: self.status_code = status_code
        self.error_code = error_code
        if error is None:
            self.error = {field: force_str(self.default_detail)}
            self.detail = {}
        else:
            self.error = error.get_errors
            self.detail = {}


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['success'] = False
        response.data['error_code'] = exc.error_code
        # response.data['status_code'] = response.status_code
        # response.data['error'] = exc.get_error
        # print(type(exc))
        response.data['error'] = exc.error
        response.data['error_msg'] = exc.error_msg

    return response
