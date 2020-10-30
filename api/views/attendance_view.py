from helper.custom_response import CustomResponse,missing_field_error_response,success_response
from rest_framework.response import Response
from rest_framework import status
from api.serializers.mark_attendance_serializer import MarkAttendanceSerializers
from helper.custom_jwt import Jwt
from helper.custom_api_view import AuthenticatedApiView


class MarkAttendance(AuthenticatedApiView):

    def post(self, request, user):
        serializer = MarkAttendanceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user)
            token = Jwt.encode(username=user.username)
            response = success_response()
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = missing_field_error_response(error=serializer.errors,error_message=str(serializer.errors))
        return Response(response.get_response, status=status.HTTP_200_OK)
