
from django.urls import path
from quiz.views import create_quiz,create_questions,Assessment_detail

app_name = 'quiz'

urlpatterns = [
    path('create/', create_quiz, name='create_quiz'),
    path('create/questions/<int:quiz_id>/', create_questions, name='create_questions'),
    path('assessment_detail/',Assessment_detail, name='Assessment_detail'),
]
