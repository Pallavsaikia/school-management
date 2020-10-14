from django.db import models
from teacher.models import UserAbstract
from courses.models import Courses
from subject.models import Subject
from django.db.models import Q
import traceback
import datetime


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class RegisterBookManager(models.Manager):
    SUBJECT_ERROR = "Subject does not exist"
    BOOK_ERROR = "Book for this year already exist"
    BOOK_NOT_AVAILABLE = "Book is not available"
    SUCCESSFULLY_ADDED = "Book is Successfully added"
    SUCCESSFULLY_UPDATED = "Book is Successfully Updated"

    def get_or_do_not_exist(self, id_book):
        try:
            qs = self.get(id=id_book)
            return True, qs
        except RegisterBook.DoesNotExist:
            print(traceback.print_exc())
            return False, None

    def toggle_book(self, id):
        exist, book = self.get_or_do_not_exist(id_book=id)
        if exist:
            book.active = not book.active
            book.save()
            return True, self.SUCCESSFULLY_UPDATED
        else:
            return False, self.BOOK_NOT_AVAILABLE

    def check_book_exist_by_year_subject(self, subject_id, year):
        try:
            exist, subject = Subject.objects.get_or_do_not_exist(id_subject=subject_id)

            if exist:
                qs = self.get_queryset().filter(subject=subject).filter(year=year)
                if qs.count() >= 1:
                    return True, self.BOOK_ERROR, subject
                else:
                    return False, self.BOOK_NOT_AVAILABLE, subject
            else:
                return True, self.SUBJECT_ERROR, subject
        except:
            print(traceback.print_exc())
            print(traceback.print_exc())
            print(traceback.print_exc())
            return False, self.BOOK_NOT_AVAILABLE, None

    def new_book(self, subject_id, year, active=True):

        exist, str, subject = self.check_book_exist_by_year_subject(subject_id=subject_id, year=year)
        if exist:
            return False, str
        else:
            RegisterBook(active=active, subject=subject, year=year).save()
            return True, self.SUCCESSFULLY_ADDED


# Create your models here.
class RegisterBook(models.Model):
    class Meta:
        unique_together = (('subject', 'year'))

    # professor = models.ForeignKey(UserAbstract, on_delete=models.CASCADE, blank=True, null=True)
    # description = models.CharField(blank=True, null=True, max_length=30)
    total_classes = models.IntegerField(blank=False, null=False, default=0)
    active = models.BooleanField(default=True)
    open = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False)
    year = models.IntegerField(default=current_year)

    objects = RegisterBookManager()

    def __str__(self):
        return self.subject.course.abbreviation + "-" + str(
            self.subject.semester) + " " + self.subject.name + "----" + str(self.year)
