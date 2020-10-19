import jwt
from helper.custom_jwt import Jwt


class TokenVerification:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        request.valid_token = True
        request.token_decode = {}
        try:
            decode = Jwt.decode(request)
            request.token_decode = decode
        except:
            request.valid_token = False

        response = self.get_response(request)
        return response