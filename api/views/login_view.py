from rest_framework.views import APIView
from helper.custom_response import (CustomResponse,
                                    missing_field_error_response,
                                    authentication_error_response,
                                    success_response)
from rest_framework.response import Response
from rest_framework import status
from api.serializers.login_serializer import LoginSerializer
from helper.custom_jwt import Jwt
from django.contrib.auth.models import auth
from helper.errors import Error


class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and not user.is_staff and not user.is_superuser:
                token = Jwt.encode(username=username)
                response = success_response(data={"token": token})
                return Response(response.get_response, status=status.HTTP_200_OK)
            else:
                e = Error()
                e.create_or_add_errors(key='username', errors='username or password does not match')
                error = e.get_errors
                response = authentication_error_response(error=error,
                                                         error_message="username or password does not match")
        else:
            error = serializer.errors
            response = missing_field_error_response(error=error)
        return Response(response.get_response, status=status.HTTP_200_OK)
