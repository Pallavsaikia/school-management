from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)?/?$', views.SearchAttendanceBookView.as_view(), name='search_book'),
    url(r'view/(?P<id>\d+)/$', views.ViewAttendanceBookView.as_view(), name='view_book'),
]
