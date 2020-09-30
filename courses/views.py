from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_superuser
from .forms import CourseForm


# Create your views here.

class CourseView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request):
        return render(request, "courses.html", {})

    @method_decorator(authenticate_superuser)
    def post(self, request):

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
