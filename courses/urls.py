from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.CourseView.as_view() , name='courses'),
]
