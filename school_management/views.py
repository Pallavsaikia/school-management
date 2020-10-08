from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib import messages
from helper.authenticate import authenticate_staff
from django.shortcuts import render
from .forms import RegisterForm
from teacher.models import UserAbstract


# Create your views here.

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, "login.html", {})

    def post(self, request):
        user = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=user, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("/dashboard/")

        else:
            messages.error(request, 'invalid id or password')
            logout(request)
            return redirect('/')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, "register.html", {})

    def post(self, request):
        form = RegisterForm(request.POST)
        valid, string = form.is_valid()
        if valid:
            data = form.cleaned_data
            exist, string, teacher = UserAbstract.objects.get_teacher_by_email_for_registration(data["email"])
            if exist:
                username = data["username"]
                password = data["password"]
                qs = User.objects.filter(username=username)
                if qs.count() == 0:
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    is_staff=True)
                    teacher.user = user
                    teacher.registered = True
                    teacher.save()
                    login(request, user)
                    return redirect("/dashboard/")
                else:
                    messages.error(request, "username exist")
            else:
                messages.error(request, string)

        else:
            messages.error(request, string)
        return redirect('/register/')
        # user = request.POST['username']
        # password = request.POST['password']
        # user = auth.authenticate(username=user, password=password)
        # if user is not None and user.is_staff:
        #     login(request, user)
        #     return redirect("/dashboard/")
        #
        # else:
        #     messages.error(request, 'invalid id or password')
        #     logout(request)
        #     return redirect('/')


class DashboardView(View):
    @method_decorator(authenticate_staff)
    def get(self, request):
        return render(request, "dashboard.html", {})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


def handler404(request, *args, **argv):
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, "500.html", {})
    response.status_code = 500
    return response
