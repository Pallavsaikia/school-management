import jwt
from school_management.settings import QR_KEY


class QrCode:
    @staticmethod
    def decode(string):
        return jwt.decode(string, QR_KEY, algorithms=["HS256"])

    @staticmethod
    def encode(book_id, date, half):
        return jwt.encode({"book_id": book_id,
                           "half": half,
                           "date": str(date)}, QR_KEY, algorithm="HS256")
