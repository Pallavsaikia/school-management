from django.http import JsonResponse
from functools import wraps
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout


def authenticate_staff(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        else:
            return function(request, *args, **kwargs)
    return wrap
