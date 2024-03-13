# models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from courses.models import Course, Module

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name=_("Title"), max_length=60, blank=False)
    # Add other fields as needed

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"), related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=False, verbose_name=_("Question"))
    mark = models.IntegerField(default=1, verbose_name=_("Mark"))  # Assuming each question has a mark

class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=False, verbose_name=_("Choice"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))

    def __str__(self):
        return self.text
