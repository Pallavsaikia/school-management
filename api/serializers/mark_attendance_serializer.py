from rest_framework import serializers
from helper.validation_error_response import error_response
from django.contrib.auth.models import User
from teacher.models import UserAbstract
from student.models import Student
from helper.custom_jwt import Jwt


class MarkAttendanceSerializers(serializers.Serializer):
    qr_scan = serializers.CharField(required=True)

    def save(self, request):
        qr_scan = self.validated_data['qr_scan']
        Jwt.decode_qr(qr_scan)
