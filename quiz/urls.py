
from django.urls import path
from quiz.views import create_quiz,create_questions

app_name = 'quiz'

urlpatterns = [
     path('create/', create_quiz, name='create_quiz'),
    path('create/questions/<int:quiz_id>/', create_questions, name='create_questions'),
]
