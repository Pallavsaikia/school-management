from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from courses.models import Courses
import traceback


class TeacherManager(models.Manager):
    pass


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(blank=False, null=False, max_length=30, default='abc')
    last_name = models.CharField(blank=False, null=False, max_length=30, default='xyz')
    email = models.EmailField(blank=False, null=False, unique=True, default='abc@gmail.com')
    # phone_number = models.BigIntegerField(blank=False, null=False, default='0', unique=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    registered = models.BooleanField(default=False)
    objects = TeacherManager()

    def __str__(self):
        return self.user.username
