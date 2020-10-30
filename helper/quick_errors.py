from helper.errors import Error
from helper.exception import CustomValidation
from helper import status_codes


def raise_internal_server_error(key=None, details=None, error: Error = None,
                                error_message: str = "An Internal error Occured"):
    if error is None:
        error = Error()
        error.create_or_add_errors(key=key, errors=details)
    raise CustomValidation(error=error, error_code=status_codes.INTERNAL_SERVER_ERROR, error_msg=error_message)


def raise_field_error(key=None, details=None, error: Error = None, error_message: str = "Field Error"):
    if error is None:
        error = Error()
        error.create_or_add_errors(key=key, errors=details)
    raise CustomValidation(error=error, error_code=status_codes.INVALID_FIELDS, error_msg=error_message)


def raise_missing_field_error(key=None, details=None, error: Error = None, error_message: str = "Field Missing"):
    if error is None:
        error = Error()
        error.create_or_add_errors(key=key, errors=details)
    raise CustomValidation(error=error, error_code=status_codes.FIELDS_MISSING, error_msg=error_message)
