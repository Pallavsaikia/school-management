from rest_framework import serializers
from helper.validation_error_response import error_response
from django.contrib.auth.models import User
from teacher.models import UserAbstract
from student.models import Student
from register_book.models import RegisterBook
from attendance.models import Attendance
from helper.qr import QrCode, QrData
import traceback
from rest_framework.serializers import ReturnDict
from helper.quick_errors import raise_field_error


class MarkAttendanceSerializers(serializers.Serializer):
    QR_ERROR = "Invalid QR CODE"
    BOOK_DOES_NOT_EXIST = "Invalid book id"
    BOOK_CLOSE_ERROR = "Book close for entry contact your teacher"
    qr_code = serializers.CharField(required=True)
    ret: ReturnDict = {}
    _errors = {}

    @property
    def errors(self):
        ret = super().errors
        # if isinstance(ret, list) and len(ret) == 1 and getattr(ret[0], 'code', None) == 'null':
        #     # Edge case. Provide a more descriptive error than
        #     # "this field may not be null", when no data is passed.
        #     detail = ErrorDetail('No data provided', code='null')
        #     ret = {api_settings.NON_FIELD_ERRORS_KEY: [detail]}
        for key, value in ReturnDict(ret, serializer=self).items():
            print(key)
            print(value)
            print(type(value))
        # print(type(ReturnDict(ret, serializer=self).keys()))
        return ReturnDict(ret, serializer=self).values()

    def is_valid(self, raise_exception=False):
        error_exist = super().is_valid()
        return error_exist and not bool(self.ret)

    def save(self, user):
        qr_scan = self.validated_data['qr_code']

        success, decode = QrCode.decode(qr_scan)
        if success:
            qr = QrData(decode)
            date = qr.get_processed_date()
            exist, book = RegisterBook.objects.get_or_do_not_exist(id_book=qr.book_id)
            if exist:
                if book.open:
                    exist, attendance = Attendance.objects.get_attendance_row_for_update(register_book=book,
                                                                                         half=qr.half,
                                                                                         date_attendance=date,
                                                                                         student=user.userabstract)

                else:
                    raise_field_error(key="Book", details=self.BOOK_CLOSE_ERROR)
            else:
                raise_field_error(key="Book", details=self.BOOK_DOES_NOT_EXIST)
        else:
            raise_field_error(key="Book", details=self.QR_ERROR)
