from django.db import models
from django.db.models import ForeignKey, CASCADE
from django.contrib.auth.models import User

# Create your models here.




class SchoolClass (models.Model):
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name
    def __repr__(self):
        return self.class_name

class StudentClass(models.Model):
    student = ForeignKey(User, on_delete=models.CASCADE)
    sclass = ForeignKey(SchoolClass, on_delete=CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.sclass.class_name}"
    def __repr__(self):
        return f"({self.student.username} - {self.sclass.class_name}"

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    teacher = ForeignKey(User, on_delete=models.CASCADE)
    sclass = ForeignKey(SchoolClass, on_delete=models.CASCADE)
    homework = models.TextField(blank=True, null=True)
    room = models.CharField(max_length=200)
    lesson_type = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.username} -{self.date}"
    def __repr__(self):
        return f"{self.name} - {self.teacher.username} -{self.date}"

class Grade (models.Model):
    student = ForeignKey(User, on_delete=models.CASCADE)
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return str(f"{self.student.username} - {self.lesson.name} -{self.grade}")
    def __repr__(self):
        return str(self.grade)