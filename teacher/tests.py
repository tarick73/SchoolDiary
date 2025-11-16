from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from common_data.models import Lesson, Grade, SchoolClass


class TeacherEndpointsTests(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.teacher = User.objects.get(username="teacher")
        self.client.force_login(self.teacher)

    def test_lessons_list_view(self):
        """
        Ендпоінт: перегляд списку уроків (GET /teacher/lessons/)
        """
        url = reverse("lessons")  # name="lessons" в teacher/urls.py
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teacher/lessons.html")
        # В контексті повинно бути поле "lessons"
        self.assertIn("lessons", response.context)
        # І там має бути хоча б один урок (з фікстури)
        self.assertGreaterEqual(response.context["lessons"].count(), 1)

    def test_create_new_lesson(self):
        """
        Ендпоінт: створення нового уроку (POST /teacher/lessons/)
        """
        url = reverse("lessons")
        school_class = SchoolClass.objects.first()

        lessons_before = Lesson.objects.count()

        data = {
            "name": "New test lesson",
            "description": "Test description",
            "date": "2025-01-01",
            "homework": "Do something",
            "room": "101",
            "sclass_id": str(school_class.pk),
        }

        response = self.client.post(url, data)

        # Должен быть redirect (302) назад на список уроков
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lesson.objects.count(), lessons_before + 1)

        # Проверяем, что урок реально создался
        new_lesson = Lesson.objects.get(name="New test lesson")
        self.assertEqual(new_lesson.teacher, self.teacher)
        self.assertEqual(new_lesson.sclass, school_class)

    def test_add_grade(self):
        """
        Ендпоінт: додавання оцінки (POST /teacher/lessons/<id>/set_grade/)
        """
        lesson = Lesson.objects.first()
        student = User.objects.get(username="student")

        grades_before = Grade.objects.count()

        url = reverse("set_grade", args=[lesson.pk])
        data = {
            "student_id": str(student.pk),
            "grade": "5",
        }

        response = self.client.post(url, data)

        # Теж очікуємо redirect на сторінку уроку
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Grade.objects.count(), grades_before + 1)

        self.assertTrue(
            Grade.objects.filter(
                student=student,
                lesson=lesson,
                grade=5,
            ).exists()
        )
