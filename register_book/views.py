from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import UserAbstract

from courses.models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_superuser


# Create your views here.

class RegisterBookView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        teacher = UserAbstract.objects.get_teacher()
        if id is None:
            return render(request, "register_book.html", {"edit": False, 'courses': courses, "teachers": teacher})
        else:
            exist, qs = UserAbstract.objects.get_or_do_not_exist(id=id)

            if exist:

                return render(request, "teachers.html",
                              {"edit": True, "teacher_edit": qs, 'courses': courses, "teachers": teacher})
            else:
                messages.error(request, 'ID does not exist')
                return render(request, "teachers.html", {"edit": False, "courses": courses, "teachers": teacher})

    # @method_decorator(authenticate_superuser)
    # def post(self, request, id=None):
    #     form = PreRegisterForm(request.POST)
    #     courseid = request.POST.get("course", "")
    #     if form.is_valid() and courseid != "":
    #
    #         data = form.cleaned_data
    #         active = request.POST.get("active", "") == "active"
    #         if id is None:
    #             qs, success, string = UserAbstract.objects.new_teacher(first_name=data["first_name"],
    #                                                                   last_name=data["last_name"],
    #                                                                   email=data["email"], courseid=courseid,
    #                                                                   active=active)
    #         else:
    #             success, string = UserAbstract.objects.update_teacher(id_teacher=id, first_name=data["first_name"],
    #                                                                  last_name=data["last_name"],
    #                                                                  email=data["email"], courseid=courseid,
    #                                                                  active=active)
    #         if success:
    #             messages.success(request, string)
    #         else:
    #             messages.error(request, string)
    #     else:
    #         messages.error(request, "Fields cannot be empty")
    #     return redirect('/teachers')