# users/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
app_name = 'users'

urlpatterns = [
    path("users/login/", LoginView.as_view(), name="login"),
    path('student/add/', views.student_add_view, name='student_add'),
    path('student/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('student/list/', views.student_list, name='student_list'),
    path('settings/', views.settings_page, name='settings'),


    path('student/profile/<int:pk>/', views.student_profile, name='student_profile'),


    path('validate-username/', views.validate_username, name='validate_username'),
]
