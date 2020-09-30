from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from helper.authenticate import authenticate_staff


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
            messages.error(request,'invalid id or password')
            logout(request)
            return redirect('/')


class DashboardView(View):
    @method_decorator(authenticate_staff)
    def get(self, request):
        return render(request, "dashboard.html", {})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")
