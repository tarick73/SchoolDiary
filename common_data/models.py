from django.db import models
from django.db.models import ForeignKey, CASCADE
from django.contrib.auth.models import User

# Create your models here.




class SchoolClass (models.Model):
    class_name = models.CharField(max_length=100)

class StudentClass(models.Model):
    student = ForeignKey(User, on_delete=models.CASCADE)
    sclass = ForeignKey(SchoolClass, on_delete=CASCADE)

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    teacher = ForeignKey(User, on_delete=models.CASCADE)
    sclass = ForeignKey(SchoolClass, on_delete=models.CASCADE)
    homework = models.TextField(blank=True, null=True)
    room = models.CharField(max_length=200)
    lesson_type = models.IntegerField(null=True, blank=True)

class Grade (models.Model):
    student = ForeignKey(User, on_delete=models.CASCADE)
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.IntegerField()