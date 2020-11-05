from django.db import models
from register_book.models import RegisterBook
from teacher.models import UserAbstract
import datetime
from django.db.models import Max


class AttendanceManager(models.Manager):
    NO_STUDENT = "No student in this course and semester"
    HALF_ERROR = "Attendance already taken for this half"
    SUCCESS = "Attendance Started"

    def get_attendance_row_for_update(self, register_book: RegisterBook, student: UserAbstract, date_attendance, half):
        qs = Attendance.objects.filter(date_attendance=date_attendance).filter(register_book=register_book).filter(
            student=student).filter(half=half)
        if qs is not None:
            if qs.count() > 0:
                return True, qs.first()
            else:
                return False, None
        else:

            return False, None

    def get_half(self, book, date_attendance):
        qs = Attendance.objects.filter(date_attendance=date_attendance).filter(register_book=book).aggregate(
            Max('half'))
        count = qs['half__max']
        if count is None:
            count = 0
        return count

    def check_entry_exist_for_date_half_book(self, book, date_attendance, half):
        qs = Attendance.objects.filter(date_attendance=date_attendance).filter(register_book=book).filter(half=half)
        if qs.count() > 0:
            return True, qs
        else:
            return False, qs

    def bulk_insert(self, book_id, half, date_attendance):
        exist, book = RegisterBook.objects.get_or_do_not_exist(id_book=book_id)
        if exist:
            # book exist
            half_last = self.get_half(book=book, date_attendance=date_attendance)
            if half_last < half:
                student_list = UserAbstract.objects.get_student_by_course_semester(course=book.subject.course,
                                                                                   semester=book.subject.semester)
                if student_list is not None:
                    # has student
                    print(str(student_list.count()))
                    if student_list.count() > 1:
                        book.open = True
                        book.total_classes = book.total_classes + 1
                        book.save()
                        # does not have student
                        for student in student_list:
                            Attendance(register_book=book, student=student, half=half,
                                       date_attendance=date_attendance).save()

                        return True, self.SUCCESS
                    else:
                        return False, self.NO_STUDENT


                else:
                    # does not have student
                    return False, self.NO_STUDENT
            else:
                # half error
                return False, self.HALF_ERROR
        else:
            # book does not exist
            return False, RegisterBook.objects.BOOK_NOT_AVAILABLE


class Attendance(models.Model):
    class Meta:
        unique_together = (('register_book', 'student', 'date_attendance', 'half'))

    register_book = models.ForeignKey(RegisterBook, on_delete=models.CASCADE, blank=False, null=False)
    student = models.ForeignKey(UserAbstract, on_delete=models.CASCADE, blank=False, null=False)
    present = models.BooleanField(default=False)
    half = models.IntegerField(default=1)
    date_attendance = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(blank=True, null=True)
    objects = AttendanceManager()

    def __str__(self):
        return str(self.register_book) + "" + str(self.date_attendance) + "" + str(self.student)
