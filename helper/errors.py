


class Error:
    error: dict = {}

    def __init__(self, errors=None):
        if errors is None:
            errors = {}
        self.error = errors

    def create_or_add_errors(self, key: str, errors: str):
        self.error[key] = [errors]

    @property
    def get_errors(self):
        return self.error

    @property
    def get_errors_dict(self):
        return {
            'error': self.error,
        }










