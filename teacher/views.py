from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import Teacher
from courses.models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_superuser


# Create your views here.

class TeacherView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        return render(request, "teachers.html", {'courses':courses})
        # courses = Teacher.objects.all()
        # if id is None:
        #     return render(request, "courses.html", {"edit": False, "courses": courses})
        # else:
        #     exist, qs = Courses.objects.get_or_do_not_exist(id)
        #     if exist:
        #         return render(request, "courses.html", {"edit": True, "course_edit": qs, "courses": courses})
        #     else:
        #         messages.error(request, 'ID does not exist')
        #         return render(request, "courses.html", {"edit": False, "courses": courses})
    #
    # @method_decorator(authenticate_superuser)
    # def post(self, request, id=None):
    #
    #     form = CourseForm(request.POST)
    #     if form.is_valid():
    #         course_name = request.POST.get("course_name", "")
    #         abbreviation = request.POST.get("abbreviation", "")
    #         num_div = request.POST.get("num_div", "")
    #         course, created = Courses.objects.new_courses(name=course_name, abbreviation=abbreviation, max_div=num_div)
    #         if created:
    #             messages.success(request, 'Successfully Added!')
    #         else:
    #             messages.error(request, 'Unique Name and Abbreviation Required')
    #         return redirect('/courses')
    #     else:
    #         messages.error(request, 'Fields cant be empty')
    #         return redirect('/courses')
