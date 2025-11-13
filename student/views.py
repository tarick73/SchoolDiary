from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from common_data.models import Lesson, Grade, StudentClass


def user_should_be_a_teacher(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if not request.user.groups.filter(name='student').exists():
            raise PermissionDenied("You must be a teacher to access this page.")
        return func(request, *args, **kwargs)
    return wrapper



@user_should_be_a_teacher
@login_required
def student_main_page(request):
    return redirect('student_lessons')

@user_should_be_a_teacher
@login_required
def lessons_list(request):
    sc = (StudentClass.objects
          .select_related('sclass')
          .filter(student=request.user)
          .first())

    if not sc:
        return render(request, 'student/lessons.html', {
            'lessons': [],
            'no_class': True
        })

    lessons = (Lesson.objects
               .select_related('teacher', 'sclass')
               .filter(sclass=sc.sclass)
               .order_by('-date', '-id'))

    return render(request, 'student/lessons.html', {
        'lessons': lessons,
        'no_class': False
    })

@user_should_be_a_teacher
@login_required
def lesson_details(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.select_related('teacher', 'sclass'),
        pk=lesson_id
    )

    my_grade = Grade.objects.filter(student=request.user, lesson=lesson).first()

    return render(request, 'student/lesson.html', {
        'lesson': lesson,
        'my_grade': my_grade,
    })

@user_should_be_a_teacher
@login_required
def my_grades(request):
    grades_qs = (Grade.objects
                 .select_related('lesson', 'lesson__teacher', 'lesson__sclass')
                 .filter(student=request.user)
                 .order_by('-lesson__date', '-id'))

    avg_grade = grades_qs.aggregate(avg=Avg('grade'))['avg']

    return render(request, 'student/my_grades.html', {
        'grades': grades_qs,
        'avg_grade': avg_grade,
    })

@user_should_be_a_teacher
def student_main_page(request):
    return redirect('student:student_lessons')
