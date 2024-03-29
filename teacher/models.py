from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from courses.models import Courses
import traceback


class UserAbstractManager(models.Manager):
    DUPLICATE_ID = "Email already in use!"
    COURSE_ERROR = "Course does not exist!"
    SUCCESS = "Successfully added!"
    SUCCESS_UPDATED = "Successfully updated!"
    USER_REGISTERED = "Email is already Registered"
    USER_NOT_FOUND = "Email not found"

    def get_student_by_course_semester(self, course:Courses, semester):
        return self.get_queryset().filter(is_staff=False).filter(registered=True).filter(active=True).filter(
            course=course).filter(student__semester=semester)

    def get_teacher(self):
        return self.get_queryset().filter(is_staff=True)

    def get_teacher_by_id(self, id_teacher):
        try:
            qs = self.get(id=id_teacher)
            if qs.is_staff and qs.active:
                return True, qs
            else:
                False, None
        except:
            False, None

    def get_teacher_by_email(self, email):
        qs = self.get_queryset().filter(is_staff=True).filter(active=True).filter(email=email)
        if qs.count() == 1:

            return True, qs.first()
        else:
            return False, None

    def get_teacher_by_email_for_registration(self, email):
        exist, qs = self.get_teacher_by_email(email=email)
        if exist:
            if qs.registered:
                return False, self.USER_REGISTERED, None
            else:
                return True, self.SUCCESS, qs
        else:
            return False, self.USER_NOT_FOUND, None

    def get_student_by_email(self, email):
        qs = self.get_queryset().filter(is_staff=False).filter(active=True).filter(email=email)
        if qs.count() == 1:
            return True, qs.first()
        else:
            return False, None

    def get_student_by_email_for_registration(self, email):
        exist, qs = self.get_student_by_email(email=email)
        if exist:
            if qs.registered:
                return False, self.USER_REGISTERED, None
            else:
                return True, self.SUCCESS, qs
        else:
            return False, self.USER_NOT_FOUND, None

    def get_teacher_by_department(self, course):
        return self.get_queryset().filter(is_staff=True).filter(active=True).filter(course=course)

    def get_student(self):
        return self.get_queryset().filter(is_staff=False)

    def get_or_do_not_exist(self, id, is_staff=True):
        try:
            qs = self.get_queryset().filter(id=id).filter(is_staff=is_staff)
            if qs.count() == 1:
                return True, qs.first()
            else:
                return False, None
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
                return UserAbstract(first_name=first_name, last_name=last_name,
                                    email=email, course=course, active=active, is_staff=True).save(), True, self.SUCCESS

    def new_student(self, first_name, last_name, email, courseid, active):
        qs = self.get_queryset().filter(email=email)
        if qs.count() == 1:
            return qs, False, self.DUPLICATE_ID
        else:
            exist, course = Courses.objects.get_or_do_not_exist(courseid)
            if not exist:
                return qs, False, self.COURSE_ERROR
            else:
                return UserAbstract(first_name=first_name, last_name=last_name,
                                    email=email, course=course, active=active,
                                    is_staff=False).save(), True, self.SUCCESS

    def update_teacher(self, id_teacher, first_name, last_name, email, courseid, active):
        qs = self.get_queryset().exclude(id=id_teacher).filter(email=email)
        if qs.count() == 1:
            return False, self.DUPLICATE_ID
        else:
            exist, course = Courses.objects.get_or_do_not_exist(courseid)
            if not exist:
                return False, self.COURSE_ERROR
            else:
                update = self.get_queryset().get(id=id_teacher)
                update.first_name = first_name
                update.last_name = last_name
                update.email = email
                update.course = course
                update.active = active
                update.save()
                return True, self.SUCCESS_UPDATED

    def update_student(self, id_student, first_name, last_name, email, courseid, active):
        qs = self.get_queryset().exclude(id=id_student).filter(email=email)
        if qs.count() == 1:
            return False, self.DUPLICATE_ID
        else:
            exist, course = Courses.objects.get_or_do_not_exist(courseid)
            if not exist:
                return False, self.COURSE_ERROR
            else:
                update = self.get_queryset().get(id=id_student)
                update.first_name = first_name
                update.last_name = last_name
                update.email = email
                update.course = course
                update.active = active
                update.save()
                return True, self.SUCCESS_UPDATED


# Create your models here.
class UserAbstract(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(blank=False, null=False, max_length=30, default='abc')
    last_name = models.CharField(blank=False, null=False, max_length=30, default='xyz')
    email = models.EmailField(blank=False, null=False, unique=True, default='abc@gmail.com')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default=None)
    # phone_number = models.BigIntegerField(blank=False, null=False, default='0', unique=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # profile_completed = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)
    objects = UserAbstractManager()

    def __str__(self):
        return self.first_name + " " + self.last_name
