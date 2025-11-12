# student/urls.py
from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path('', views.student_main_page, name='student_dashboard'),
    path('lessons/', views.lessons_list, name='student_lessons'),
    path('lessons/<int:lesson_id>/', views.lesson_details, name='student_lesson_details'),
    path('my-grades/', views.my_grades, name='student_my_grades'),
]
