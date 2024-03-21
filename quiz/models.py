from django.db import models
from courses.models import Course,Module,Chapter


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,null=True)
    total_questions = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.module.title

class QuesModel(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,null=True)
    question = models.CharField(max_length=200,default=0)
    op1 = models.CharField(max_length=200,default=0)
    op2 = models.CharField(max_length=200,default=0)
    op3 = models.CharField(max_length=200,default=0)
    op4 = models.CharField(max_length=200,default=0)
    ans = models.CharField(max_length=200,default=0)

    def __str__(self):
        return self.question