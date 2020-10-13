from django.db import models
from teacher.models import UserAbstract
from courses.models import Courses
from subject.models import Subject
import datetime


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class RegisterBookManager(models.Manager):
    pass


# Create your models here.
class RegisterBook(models.Model):
    professor = models.ForeignKey(UserAbstract, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(blank=True, null=True, max_length=30)
    total_classes = models.IntegerField(blank=False, null=False, default=0)
    active = models.BooleanField(default=True)
    open = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False)
    year = models.IntegerField(default=current_year)

    objects = RegisterBookManager()

    def __str__(self):
        return self.subject.course.abbreviation + "-" + str(self.subject.semester) + " " + self.subject.name + "----" + str(self.year)
