from rest_framework import serializers

from register_book.models import RegisterBook
from attendance.models import Attendance
from helper.qr import QrCode, QrData
from datetime import datetime
from helper.quick_errors import raise_field_error, raise_internal_server_error


class MarkAttendanceSerializers(serializers.Serializer):
    QR_ERROR = "Invalid QR CODE"
    BOOK_DOES_NOT_EXIST = "Invalid book id"
    BOOK_CLOSE_ERROR = "Book close for entry contact your teacher"
    NO_ENTRY_FOR_ATTENDANCE_EXIST = "No entry for this qr code"
    qr_code = serializers.CharField(required=True)

    def save(self, user):
        qr_scan = self.validated_data['qr_code']

        success, decode = QrCode.decode(qr_scan)
        if success:
            qr = QrData(decode)
            valid, date = qr.get_processed_date()
            exist, book = RegisterBook.objects.get_or_do_not_exist(id_book=qr.book_id)
            if exist and valid:
                if book.open:
                    exist, attendance = Attendance.objects.get_attendance_row_for_update(register_book=book,
                                                                                         half=qr.half,
                                                                                         date_attendance=date,
                                                                                         student=user.userabstract)
                    if exist:
                        attendance.present = True
                        attendance.updated_at = datetime.now()
                        attendance.save()
                    else:
                        raise_internal_server_error(key="Attendance", error_message=self.NO_ENTRY_FOR_ATTENDANCE_EXIST)

                else:
                    raise_field_error(key="Book", error_message=self.BOOK_CLOSE_ERROR)
            else:
                raise_field_error(key="Book", error_message=self.BOOK_DOES_NOT_EXIST)
        else:
            raise_field_error(key="Book", error_message=self.QR_ERROR)
