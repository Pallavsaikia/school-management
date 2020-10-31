from rest_framework.views import APIView
from helper.custom_response import CustomResponse
from rest_framework.response import Response
from rest_framework import status
from api.serializers.registration_serializer import RegisterSerializers
from helper.custom_jwt import Jwt
from helper.custom_response import missing_field_error_response, success_response
from django.contrib.auth.models import User


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data['username']
            user = User.objects.get(username=username)
            token = Jwt.encode(username=username)
            response = success_response(data={"token": token,
                                              "username": username,
                                              "first_name": user.userabstract.first_name,
                                              "last_name": user.userabstract.last_name,
                                              "email": user.userabstract.email})
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = missing_field_error_response(error=serializer.errors, error_message=str(serializer.errors))
        return Response(response.get_response, status=status.HTTP_200_OK)
