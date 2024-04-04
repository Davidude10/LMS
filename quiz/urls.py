
from django.urls import path
from quiz import views

app_name = 'quiz'

urlpatterns = [

    path("<int:myid>/", views.quiz, name="quiz"), 
    path('<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    path('<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
    
    path('add_quiz/', views.add_quiz, name='add_quiz'),    
    path('add_question/', views.add_question, name='add_question'),  
    path('add_options/<int:myid>/', views.add_options, name='add_options'),
    path('assessment_detail/',views.Assessment_detail, name='Assessment_detail'),
]
