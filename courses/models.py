from django.db import models


# Create your models here.
class Courses(models.Model):
    name = models.CharField(blank=False, null=False, unique=True,max_length=20)
    max_div = models.IntegerField(default=6, blank=False, null=False)

    def __str__(self):
        return self.name
