from rest_framework.views import APIView
from helper.custom_response import CustomResponse
from rest_framework.response import Response
from rest_framework import status
from api.serializers.registration_serializer import RegisterSerializers
from helper.custom_jwt import Jwt


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data['username']
            token = Jwt.encode(username=username)
            response = CustomResponse(success=True,data={"token":token})
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = CustomResponse(success=False, error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
