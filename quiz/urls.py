
from django.urls import path
from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('add_question/', views.add_question, name='add_question'),
    path('assessment_detail/',views.Assessment_detail, name='Assessment_detail'),
]
