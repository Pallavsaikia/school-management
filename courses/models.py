from django.db import models
from django.db.models import Q


class CoursesManager(models.Manager):
    def new_courses(self, name, abbreviation, max_div=6):
        qs = self.get_queryset().filter(Q(name=name) | Q(abbreviation=abbreviation))
        if qs.count() == 1:
            return qs, False
        else:
            return Courses(name=name, abbreviation=abbreviation, max_div=max_div).save(), True


# Create your models here.
class Courses(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, max_length=20)
    abbreviation = models.CharField(blank=False, null=False, unique=True, max_length=6, default='abc')
    max_div = models.IntegerField(default=6, blank=False, null=False)

    objects = CoursesManager()

    def __str__(self):
        return self.name
