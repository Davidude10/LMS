
from django.urls import path
from quiz.views import Quizpage,addQuestion

app_name = 'quiz'

urlpatterns = [
    path('quizpage', Quizpage,name='Quizpage'),
    path('addQuestion/', addQuestion,name='addQuestion'),
]
