# quiz/models.py

from django.db import models
from django.conf import settings
from courses.models import Module

class Quiz(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"Quiz for {self.module}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, default=None)
    text = models.TextField(max_length=200, blank=True, null=True)
    correct_answer = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, default=None)
    text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, default=None)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s attempt on {self.quiz}"
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, default=None)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s attempt on {self.quiz}"