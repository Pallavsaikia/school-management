from django.db import models
from teacher.models import UserAbstract
import datetime


def current_year():
    return datetime.date.today().year


class StudentManager(models.Manager):
    pass


# Create your models here.
class Student(models.Model):
    student = models.OneToOneField(UserAbstract, on_delete=models.CASCADE, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True, default='1')
    year = models.IntegerField(default=current_year())

    objects = StudentManager()

    def __str__(self):
        return self.student
