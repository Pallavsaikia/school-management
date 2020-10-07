from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from courses.models import Courses
import traceback


class PreRegisterManager(models.Manager):
    DUPLICATE_ID = "Email already in use!"
    COURSE_ERROR = "Course does not exist!"
    SUCCESS = "Successfully added!"

    def get_or_do_not_exist(self, id):
        try:
            qs = self.get(id=id)
            return True, qs
        except:
            return False, None

    def new_teacher(self, first_name, last_name, email, courseid, active):
        qs = self.get_queryset().filter(email=email)
        if qs.count() == 1:
            return qs, False, self.DUPLICATE_ID
        else:
            exist, course = Courses.objects.get_or_do_not_exist(courseid)
            if not exist:
                return qs, False, self.COURSE_ERROR
            else:
                return PreRegister(first_name=first_name, last_name=last_name,
                                   email=email, course=course, active=active, is_staff=True).save(), True, self.SUCCESS


# Create your models here.
class PreRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(blank=False, null=False, max_length=30, default='abc')
    last_name = models.CharField(blank=False, null=False, max_length=30, default='xyz')
    email = models.EmailField(blank=False, null=False, unique=True, default='abc@gmail.com')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default=None)
    # phone_number = models.BigIntegerField(blank=False, null=False, default='0', unique=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)
    objects = PreRegisterManager()

    def __str__(self):
        return self.first_name + " " + self.last_name
