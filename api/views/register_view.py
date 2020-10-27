from rest_framework.views import APIView
from helper.custom_response import CustomResponse
from rest_framework.response import Response
from rest_framework import status
from api.serializers.registration_serializer import RegisterSerializers
from helper.custom_jwt import Jwt
from helper.custom_response import missing_field_error_response, success_response


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data['username']
            token = Jwt.encode(username=username)
            response = success_response(data={"token": token})
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = missing_field_error_response(error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_200_OK)
