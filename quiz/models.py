from django.db import models
from courses.models import Course,Module,Chapter
from Learning import settings


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,null=True)
    total_questions = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.module.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Attempt by {self.student.username} on {self.quiz.module.title} quiz"