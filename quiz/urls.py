
from django.urls import path
from quiz.views import create_quiz, add_questions,add_choices

app_name = 'quiz'

urlpatterns = [
    path('modules/<int:module_id>/create-quiz/', create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-questions/', add_questions, name='add_questions'),
    path('<int:quiz_id>/add-choices/<int:question_id>/',add_choices, name='add_choices'),
]
