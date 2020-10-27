from django.http import JsonResponse
from functools import wraps
from django.contrib.auth.models import User


def check_token(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.valid_token:
            return JsonResponse({"success": False,
                                 "error": {"token": "invalid token"},
                                 "data": {}})
        else:
            username = request.token_decode.get("username")
            user = User.objects.get(username=username)
            # if User.objects.filter(username=username).exists():
            if user is not None and not user.is_staff and not user.is_superuser:
                return function(request, user, *args, **kwargs)
            else:
                return JsonResponse({"success": False,
                                     "error": {"token": "invalid token"},
                                     "data": {}})

    return wrap
