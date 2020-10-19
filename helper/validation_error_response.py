
class CustomResponse:
    error = {}
    success = ""
    last_page = 0

    def __init__(self, success=True,  error=None, last_page=0):

        self.error = error
        self.success = success
        self.last_page = last_page

    @property
    def get_response(self):
        if self.last_page == 0:
            return {
                'success': self.success,
                'error': self.error,

            }
        else:
            return {
                'success': self.success,
                'error': self.error,
                'last_page': self.last_page
            }


def error_response(error):
    return CustomResponse(success=False, error=error)
