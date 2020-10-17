from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    data = {}
    error = {}
    success = ""
    last_page = 0

    def __init__(self, success=True, data=None, error=None, last_page=0):
        self.data = data
        self.error = error
        self.success = success
        self.last_page = last_page

    @property
    def get_response(self):
        if self.last_page == 0:
            return {
                'success': self.success,
                'error': self.error,
                'data': self.data
            }
        else:
            return {
                'success': self.success,
                'error': self.error,
                'data': self.data,
                'last_page':self.last_page
            }