from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from courses.models import Courses
from django.contrib import messages
from helper.authenticate import authenticate_staff


class GetSemester(View):
    @method_decorator(authenticate_staff)
    def post(self, request):
        course_id = request.POST.get("course", "")
        if course_id != "":
            exist, course = Courses.objects.get_or_do_not_exist(id_course=course_id)
            if exist:
                json_data = {"success": True, "semester": course.max_div+1}
            else:
                json_data = {"success": False, "semester": []}
        else:
            json_data = {"success": False, "semester": []}
        return JsonResponse(json_data)
