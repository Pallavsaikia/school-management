from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import PreRegister
from .forms import TeacherForm
from courses.models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_superuser


# Create your views here.

class TeacherView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        return render(request, "teachers.html", {'courses': courses})
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

    @method_decorator(authenticate_superuser)
    def post(self, request, id=None):
        form = TeacherForm(request.POST)
        courseid = request.POST.get("course", "")
        if form.is_valid() and courseid != "":

            data = form.cleaned_data
            active = request.POST.get("active", "") == "active"
            qs, success, string = PreRegister.objects.new_teacher(first_name=data["first_name"],
                                                                  last_name=data["last_name"],
                                                                  email=data["email"], courseid=courseid, active=active)
            if success:
                messages.success(request, string)
            else:
                messages.error(request, string)
        else:
            messages.error(request, "Fields cannot be empty")
        return redirect('/teachers')
