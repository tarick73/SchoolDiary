from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
import common_data.views

def root_redirect(request):
    return redirect('lessons')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('login/',    common_data.views.login_handler,    name='login'),
    path('logout/',   common_data.views.logout_handler,   name='logout'),
    path('register/', common_data.views.register_handler, name='register'),
    path('profile/',  common_data.views.profile_view,     name='profile'),
    path("student/", include("student.urls")),
    path("teacher/", include("teacher.urls")),
]
