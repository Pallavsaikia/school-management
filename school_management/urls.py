"""school_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static


handler404 = 'school_management.views.handler404'
handler500 = 'school_management.views.handler500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
    url(r'dashboard/', views.DashboardView.as_view(), name='dashboard'),
    url(r'^courses/', include(('courses.urls', 'courses'), namespace='courses')),
    url(r'^teachers/',  include(('teacher.urls', 'teacher'), namespace='teachers')),
    url(r'^students/',  include(('student.urls', 'student'), namespace='students')),
    url(r'^register-book/',  include(('register_book.urls', 'register_book'), namespace='register_books')),
    url(r'^attendance/',  include(('attendance.urls', 'attendance'), namespace='attendances')),
    url(r'^api/',  include(('api.urls', 'api'), namespace='apis')),
    url(r'^ajax/',  include(('ajaxapi.urls', 'ajaxapi'), namespace='ajax_apis')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
