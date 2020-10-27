from helper.custom_response import CustomResponse
from rest_framework.response import Response
from rest_framework import status
from api.serializers.mark_attendance_serializer import MarkAttendanceSerializers
from helper.custom_jwt import Jwt
from helper.custom_api_view import AuthenticatedApiView


class MarkAttendance(AuthenticatedApiView):

    def post(self, request, user):
        serializer = MarkAttendanceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            qr_code = serializer.data['qr_code']
            token = Jwt.encode(username=user.username)
            response = CustomResponse(success=True, data={"token": token})
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = CustomResponse(success=False, error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
