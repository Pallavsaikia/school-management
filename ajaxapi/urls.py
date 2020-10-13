from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^(?P<id>\d+)?/?$', views.RegisterBookView.as_view(), name='get_course_details'),
    url(r'get-semester-list/$', views.GetSemester.as_view(), name='get_semester_list'),
    url(r'get-subject-list/$', views.GetSubjects.as_view(), name='get_subject_list'),
]
