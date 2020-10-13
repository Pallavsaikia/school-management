from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import Courses
from subject.models import Subject
from django.contrib import messages
from helper.authenticate import authenticate_superuser
from .forms import CourseForm, CourseFormUpdate, SubjectForm
from teacher.models import UserAbstract


# Create your views here.

class CourseView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        if id is None:
            return render(request, "courses.html", {"edit": False, "courses": courses})
        else:
            exist, qs = Courses.objects.get_or_do_not_exist(id)
            if exist:
                return render(request, "courses.html", {"edit": True, "course_edit": qs, "courses": courses})
            else:
                messages.error(request, 'ID does not exist')
                return render(request, "courses.html", {"edit": False, "courses": courses})

    @method_decorator(authenticate_superuser)
    def post(self, request, id=None):

        form = CourseForm(request.POST)
        if form.is_valid():
            course_name = request.POST.get("course_name", "")
            abbreviation = request.POST.get("abbreviation", "")
            num_div = request.POST.get("num_div", "")
            course, created = Courses.objects.new_courses(name=course_name, abbreviation=abbreviation, max_div=num_div)
            if created:
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request, 'Unique Name and Abbreviation Required')
            return redirect('/courses')
        else:
            messages.error(request, 'Fields cant be empty')
            return redirect('/courses')


class CourseViewDelete(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        if id is not None:
            deleted = Courses.objects.delete_courses(id)
            if deleted:
                messages.success(request, 'Successfully Delete!')
            else:
                messages.error(request, 'ID does not exist')
            return redirect('/courses')
        else:
            messages.error(request, 'ID cant be empty')
            return redirect('/courses')


class CourseViewUpdate(View):
    @method_decorator(authenticate_superuser)
    def post(self, request):
        form = CourseFormUpdate(request.POST)
        if form.is_valid():
            course_name = request.POST.get("course_name", "")
            abbreviation = request.POST.get("abbreviation", "")
            num_div = request.POST.get("num_div", "")
            id = request.POST.get("id", "")
            updated, message = Courses.objects.update_course(id_course=id, name=course_name, abbreviation=abbreviation,
                                                             max_div=num_div)
            if updated:
                messages.success(request, message)
            else:
                messages.error(request, message)

            return redirect('/courses')
        else:
            messages.error(request, "invalid form field")
            return redirect('/courses')


class SemesterListView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id):
        exist, course = Courses.objects.get_or_do_not_exist(id)
        if exist:
            return render(request, "semesters.html", {'course': course})
        else:
            return redirect('/courses')


class SemesterSubjectView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, courseid, semester, subject=None):

        exist, course = Courses.objects.get_or_do_not_exist(courseid)

        if exist:
            teacher = UserAbstract.objects.get_teacher_by_department(course)
            if int(semester) <= course.max_div:
                subjects = Subject.objects.get_by_course_and_semester_all(id_course=courseid,semester=semester)
                if subject is None:
                    return render(request, "subjects.html",
                                  {'subjects': subjects, 'teachers': teacher, 'course': course, 'semester': semester,
                                   "edit": False})
                else:
                    exist, subject_edit = Subject.objects.get_or_do_not_exist(subject)

                    if exist:
                        return render(request, "subjects.html",
                                      {'subject_edit': subject_edit, 'teachers': teacher, 'subjects': subjects,
                                       'course': course,
                                       'semester': semester, "edit": True})
                    else:
                        messages.error(request, 'subject id doesnt exist')
                        return render(request, "subjects.html",
                                      {'subjects': subjects, 'teachers': teacher, 'course': course,
                                       'semester': semester, "edit": False})
            else:
                return redirect('/courses')
        else:
            return redirect('/courses')

    @method_decorator(authenticate_superuser)
    def post(self, request, courseid, semester, subject=None):

        form = SubjectForm(request.POST)
        teacherid = request.POST.get("teacher", "")
        if teacherid == "":
            teacherid = None
        if form.is_valid():
            active = request.POST.get("active", "") == "active"
            data = form.cleaned_data
            exist, course = Courses.objects.get_or_do_not_exist(courseid)
            if exist:
                if int(semester) <= course.max_div:
                    if subject is None:
                        success, string = Subject.objects.new_subject(name=data['subject_name'], course=course
                                                                      , semester=data['semester'], active=active
                                                                      , teacher_id=teacherid)
                    else:
                        success, string = Subject.objects.update_subject(id=subject, name=data['subject_name'],
                                                                         course=course
                                                                         , semester=data['semester'], active=active,
                                                                         teacher_id=teacherid)
                    if success:
                        messages.success(request, string)
                        return redirect(reverse('courses:subject', kwargs={'courseid': courseid, 'semester': semester}))
                    else:
                        messages.error(request, string)
                        return redirect(reverse('courses:subject', kwargs={'courseid': courseid, 'semester': semester}))
                else:
                    return redirect('/courses')
            else:
                return redirect('/courses')
        else:
            messages.error(request, "Invalid form fields")
            return redirect(reverse('courses:subject', kwargs={'courseid': courseid, 'semester': semester}))
