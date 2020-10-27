from school_management.settings import DATE_INPUT_FORMATS_STR
from datetime import datetime


def date_to_string(date):
    return date.strftime(DATE_INPUT_FORMATS_STR)


def string_to_date(date):
    return datetime.strptime(date, DATE_INPUT_FORMATS_STR)
