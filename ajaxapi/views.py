from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from courses.models import Courses
from subject.models import Subject
from helper.authenticate import authenticate_staff
from django.db.models import F


class GetSemester(View):
    @method_decorator(authenticate_staff)
    def post(self, request):
        course_id = request.POST.get("course", "")
        if course_id != "":
            exist, course = Courses.objects.get_or_do_not_exist(id_course=course_id)
            if exist:
                json_data = {"success": True, "semester": course.max_div + 1}
            else:
                json_data = {"success": False, "semester": []}
        else:
            json_data = {"success": False, "semester": []}
        return JsonResponse(json_data)


class GetSubjects(View):
    @method_decorator(authenticate_staff)
    def post(self, request):
        course_id = request.POST.get("course", "")
        semester = request.POST.get("semester", "")
        if course_id != "" and semester != "":
            subjects = Subject.objects.get_by_course_and_semester(id_course=course_id, semester=semester)
            if subjects is not None:
                json_data = {"success": True, "subjects": list(subjects.values('id',
                                                                               'name',
                                                                               'teacher_id',
                                                                               teacher_fname=F('teacher__first_name'),
                                                                               teacher_lname=F('teacher__last_name'),
                                                                               teacher_uname=F('teacher__user')))}
            else:
                json_data = {"success": False, "subjects": []}
        else:
            json_data = {"success": False, "subjects": []}
        return JsonResponse(json_data, safe=False)
