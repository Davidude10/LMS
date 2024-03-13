from django.db import models
from django.urls import reverse

from users.models import Student
from core.models import Session
from courses.models import Course


class TakenCourseManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="taken_courses")
    assignment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    quiz = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.course.slug})

    def __str__(self):
        return "{0} ({1})".format(self.course.title, self.course.code)

    # @staticmethod
    def get_total(self, assignment, quiz, final_exam):
        return (
            float(assignment)
            + float(quiz)
            + float(final_exam)
        )

    
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark=models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    