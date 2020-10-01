from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)?/?$', views.CourseView.as_view(), name='courses'),
    url(r'delete/(?P<id>\d+)?/?$', views.CourseViewDelete.as_view(), name='delete_course'),
    url(r'update/$', views.CourseViewUpdate.as_view(), name='update_course'),
    url(r'view/(?P<id>\d+)?/?$', views.SemesterListView.as_view(), name='view_semester_list'),
    # url(r'(?P<semester>\d+)?/?semester/$', views.SemesterView.as_view(), name='semester_list'),
]
