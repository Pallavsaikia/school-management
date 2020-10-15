from django.db import models
from register_book.models import RegisterBook
from teacher.models import UserAbstract
import datetime


class AttendanceManager(models.Manager):
    pass


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
