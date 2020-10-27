import jwt
from school_management.settings import QR_KEY
from helper.date import date_to_string, string_to_date


class QrCode:
    @staticmethod
    def decode(string):
        try:
            return True, jwt.decode(string, QR_KEY, algorithms=["HS256"])
        except:
            return False, {}

    @staticmethod
    def encode(book_id, date, half):
        return jwt.encode({"book_id": book_id,
                           "half": half,
                           "date": date_to_string(date=date)}, QR_KEY, algorithm="HS256")


class QrData:
    book_id: int
    date: str
    half: int

    def __init__(self, qr: dict):
        self.book_id = qr.get("book_id")
        self.date = qr.get("date")
        self.half = qr.get("half")

    def get_processed_date(self):
        return string_to_date(self.date)
