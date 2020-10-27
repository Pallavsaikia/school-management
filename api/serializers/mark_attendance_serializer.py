from rest_framework import serializers
from helper.validation_error_response import error_response
from django.contrib.auth.models import User
from teacher.models import UserAbstract
from student.models import Student
from helper.custom_jwt import Jwt


class MarkAttendanceSerializers(serializers.Serializer):
    QR_ERROR = {'qr_code': "Invalid QR CODE"}
    qr_code = serializers.CharField(required=True)

    def save(self):
        qr_scan = self.validated_data['qr_code']

        try:
            decode = Jwt.decode_qr(qr_scan)

        except:
            error = error_response(error=self.QR_ERROR)
            raise serializers.ValidationError(error.get_response)
