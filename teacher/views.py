from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from common_data.models import Lesson, StudentClass, Grade, SchoolClass


@login_required
def teacher_dashboard(request):
    return redirect('lessons')


@method_decorator(login_required, name='dispatch')
class Lessons(View):
    def get(self, request, *args, **kwargs):
        lessons = Lesson.objects.all().select_related('teacher')
        classes = SchoolClass.objects.all()
        return render(request, "teacher/lessons.html", {"lessons": lessons, "classes": classes})

    def post(self, request, *args, **kwargs):
        current_class_id = int(request.POST["sclass_id"])
        current_class = get_object_or_404(SchoolClass, pk=current_class_id)

        lesson = Lesson(
            name=request.POST["name"].strip(),
            description=request.POST.get("description", "").strip(),
            date=request.POST["date"],
            homework=request.POST.get("homework", "").strip(),
            room=request.POST.get("room", "").strip(),
            teacher=request.user,
            sclass=current_class,
        )
        lesson.save()
        return redirect(f"/teacher/lessons/#lesson_{lesson.id}")


def lesson_details(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)

    grades = (Grade.objects
              .filter(lesson=lesson)
              .select_related('student')
              .order_by('student__last_name', 'student__first_name', 'student__username'))

    students = (StudentClass.objects
                .filter(sclass=lesson.sclass)
                .select_related('student')
                .order_by('student__last_name', 'student__first_name', 'student__username'))

    return render(request, "teacher/lesson.html", {
        "lesson": lesson,
        "grades": grades,
        "students": students,
    })

def set_grade(request, lesson_id):
    if request.method == "POST":
        current_student = get_object_or_404(User, pk=int(request.POST["student_id"]))
        current_grade = Grade(
            grade=int(request.POST["grade"]),
            student=current_student,
            lesson=get_object_or_404(Lesson, pk=lesson_id),
        )
        current_grade.save()
        return redirect(f"/teacher/lessons/{lesson_id}/")
