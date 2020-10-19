from django.conf.urls import url
from api.views import register_view as rv
from django.urls import path, include

urlpatterns = [
    # url(r'^(?P<id>\d+)?/?$', views.SearchAttendanceBookView.as_view(), name='search_book'),
    # url(r'view/(?P<id>\d+)/$', views.ViewAttendanceBookView.as_view(), name='view_book'),
    # url(r'^login/', include(('login.urls', 'login'), namespace='login')),
    # url(r'^register/', include(('api.registration.urls', 'registration'), namespace='registration')),
    url(r'^register/', rv.RegisterApiView.as_view(), name='asd'),
]
