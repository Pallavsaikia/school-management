import jwt
from school_management.settings import TOKEN_KEY, QR_KEY


class Jwt:
    @staticmethod
    def decode(request):
        token = request.META['HTTP_AUTHORIZATION']
        return jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])



    @staticmethod
    def encode(username):
        return jwt.encode({"username": username}, TOKEN_KEY, algorithm="HS256")


