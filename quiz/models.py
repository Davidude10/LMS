# quiz/models.py

from django.db import models
from django.conf import settings
from courses.models import Module,Course
from users.models import User

class Quiz(models.Model):
    Quiz_name = models.CharField(max_length=50, null=True) 
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    Module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)

    number_of_questions = models.IntegerField(default=1, null=True)
    time = models.IntegerField(help_text="Duration of the quiz in seconds", default=1, null=True)
    
    def __str__(self):
        return self.Quiz_name

    def get_questions(self):
        return self.question_set.all()
    def save(self, *args, **kwargs):
        if self.Course:
            self.Module = Module.objects.filter(course=self.Course).first()
        super().save(*args, **kwargs)


class Question(models.Model):
    Question = models.CharField(max_length=200, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Question
    
    def get_answers(self):
        return self.answer_set.all()
    
    
class Choice(models.Model):
    Choice = models.CharField(max_length=200, null=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"question: {self.question.Question}, answer: {self.Choice}, correct: {self.correct}"
    
class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)     #########################################
    score = models.FloatField(null=True)
    
    def __str__(self):
        return str(self.quiz)