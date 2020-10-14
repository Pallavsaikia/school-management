from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import RegisterBook
from .forms import RegisterBookForm
from courses.models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_superuser


# Create your views here.

class RegisterBookView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        books = RegisterBook.objects.all().order_by('-active','-year','subject__course__abbreviation','subject__semester')
        if id is not None:
            RegisterBook.objects.toggle_book(id=id)
            return redirect('/register-book')
        else:
            return render(request, "register_book.html", {"edit": False, 'courses': courses,'books':books})

    @method_decorator(authenticate_superuser)
    def post(self, request, id=None):
        form = RegisterBookForm(request.POST)
        if form.is_valid():
            active = request.POST.get("active", "") == "active"
            data = form.cleaned_data
            success, str = RegisterBook.objects.new_book(subject_id=data["subject"],
                                                         year=data["year"],
                                                         active=active)
            if success:
                messages.success(request, str)
            else:
                messages.error(request, str)
            return redirect('/register-book')
        else:
            messages.error(request, "Fields cannot be empty")
            return redirect('/register-book')
