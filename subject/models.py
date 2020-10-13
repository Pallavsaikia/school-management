from django.db import models
from django.db.models import Q
from courses.models import Courses
from teacher.models import UserAbstract
import traceback


# Create your models here.
class SubjectManager(models.Manager):
    ID_DOES_NOT_EXIST = "Id does not exist"
    SUCCESS = "Successfully updated!"
    FIELD_ERROR = "This course and semester already has the subject"

    def get_by_course_and_semester(self, id_course, semester,active=True):
        exist, course = Courses.objects.get_or_do_not_exist(id_course)
        if exist:
            qs = self.get_queryset().filter(Q(course=course) & Q(semester=semester) & Q(active=active))
            if qs.count() >= 1:
                return qs
            else:
                return None
        else:
            return None

    def get_by_course_and_semester_all(self, id_course, semester):
        exist, course = Courses.objects.get_or_do_not_exist(id_course)
        if exist:
            qs = self.get_queryset().filter(Q(course=course) & Q(semester=semester) )
            if qs.count() >= 1:
                return qs
            else:
                return None
        else:
            return None

    def get_or_do_not_exist(self, id_subject):
        try:
            qs = self.get(id=id_subject)
            return True, qs
        except Subject.DoesNotExist:
            print(traceback.print_exc())
            return False, None

    def check_if_exist(self, name, course, semester):
        qs = self.get_queryset().filter(Q(name=name) & Q(course=course) & Q(semester=semester))

        if qs.count() >= 1:
            return True
        else:
            return False

    def new_subject(self, name, course, semester, teacher_id=None, active=True):

        if self.check_if_exist(name, course, semester):
            return False, self.FIELD_ERROR
        else:
            if teacher_id is not None:
                exist, teacher = UserAbstract.objects.get_teacher_by_id(teacher_id)
                Subject(name=name, semester=semester, course=course, active=active, teacher=teacher).save()
            else:
                Subject(name=name, semester=semester, course=course, active=active).save()
            return True, self.SUCCESS

    def update_subject(self, id, name, course, semester, teacher_id=None, active=True):
        exist, subject = self.get_or_do_not_exist(id)
        if exist:

            qs = self.get_queryset().exclude(id=id).filter(Q(name=name) & Q(course=course) & Q(semester=semester))

            if qs.count() == 1:
                return False, self.FIELD_ERROR
            else:
                subject.name = name
                subject.active = active
                if teacher_id is not None:
                    exist, teacher = UserAbstract.objects.get_teacher_by_id(teacher_id)
                    subject.teacher = teacher
                else:
                    subject.teacher = None
                subject.save()
                return True, self.SUCCESS
        else:
            return False, self.ID_DOES_NOT_EXIST


class Subject(models.Model):
    class Meta:
        unique_together = (('semester', 'course', 'name'))

    name = models.CharField(blank=False, null=False, max_length=30)
    semester = models.IntegerField(blank=False, null=False, default='0')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    teacher = models.ForeignKey(UserAbstract, on_delete=models.CASCADE, null=True, blank=True, default=None)
    active = models.BooleanField(default=True)
    objects = SubjectManager()

    def __str__(self):
        return self.course.name + str(self.semester) + " " + self.name

