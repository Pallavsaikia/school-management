from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from teacher.models import UserAbstract
from teacher.forms import PreRegisterForm
from courses.models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_superuser


# Create your views here.

class StudentView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        student = UserAbstract.objects.get_student()
        if id is None:
            return render(request, "students.html", {"edit": False, 'courses': courses, "students": student})
        else:
            exist, qs = UserAbstract.objects.get_or_do_not_exist(id=id,is_staff=False)

            if exist:

                return render(request, "students.html",
                              {"edit": True, "student_edit": qs, 'courses': courses, "students": student})
            else:
                messages.error(request, 'ID does not exist')
                return render(request, "students.html", {"edit": False, "courses": courses, "students": student})

    @method_decorator(authenticate_superuser)
    def post(self, request, id=None):
        form = PreRegisterForm(request.POST)
        courseid = request.POST.get("course", "")
        if form.is_valid() and courseid != "":

            data = form.cleaned_data
            active = request.POST.get("active", "") == "active"
            if id is None:
                qs, success, string = UserAbstract.objects.new_student(first_name=data["first_name"],
                                                                      last_name=data["last_name"],
                                                                      email=data["email"], courseid=courseid,
                                                                      active=active)
            else:
                success, string = UserAbstract.objects.update_student(id_student=id, first_name=data["first_name"],
                                                                     last_name=data["last_name"],
                                                                     email=data["email"], courseid=courseid,
                                                                     active=active)
            if success:
                messages.success(request, string)
            else:
                messages.error(request, string)
        else:
            messages.error(request, "Fields cannot be empty")
        return redirect('/students')
