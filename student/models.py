from django.db import models
from teacher.models import UserAbstract


class StudentManager(models.Manager):
    pass


# Create your models here.
class Student(models.Model):
    student = models.OneToOneField(UserAbstract, on_delete=models.CASCADE, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True, default='1')

    objects = StudentManager()

    def __str__(self):
        return self.student
