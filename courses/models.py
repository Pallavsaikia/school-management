from django.db import models
from django.db.models import Q
import traceback


class CoursesManager(models.Manager):
    ID_DOES_NOT_EXIST = "Id does not exist"
    SUCCESS = "Successfully updated!"
    FIELD_ERROR = "ID or Abbreviation must be unique"

    def get_or_do_not_exist(self, id_course):
        try:
            qs = self.get(id=id_course)
            return True, qs
        except:
            return False, None

    def update_course(self, id_course, name, abbreviation, max_div=6):
        exist, course = self.get_or_do_not_exist(id_course)
        if exist:

            qs = self.get_queryset().exclude(id=id_course).filter(Q(name=name) | Q(abbreviation=abbreviation))

            if qs.count() == 1:
                return False, self.FIELD_ERROR
            else:
                course.name = name
                course.abbreviation = abbreviation
                course.max_div = max_div
                course.save()
                return True, self.SUCCESS
        else:
            return False, self.ID_DOES_NOT_EXIST

    def new_courses(self, name, abbreviation, max_div=6):
        qs = self.get_queryset().filter(Q(name=name) | Q(abbreviation=abbreviation))
        if qs.count() == 1:
            return qs, False
        else:
            return Courses(name=name, abbreviation=abbreviation, max_div=max_div).save(), True

    def delete_courses(self, id_course):
        try:
            qs = self.get(id=id_course)
            qs.delete()
            return True
        except:
            return False


# Create your models here.
class Courses(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, max_length=20)
    abbreviation = models.CharField(blank=False, null=False, unique=True, max_length=6, default='abc')
    max_div = models.IntegerField(default=6, blank=False, null=False)

    objects = CoursesManager()

    def __str__(self):
        return self.name
