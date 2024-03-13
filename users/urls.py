# users/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
app_name = 'users'

urlpatterns = [
    path("users/login/", LoginView.as_view(), name="login"),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/', views.profile_single, name='profile_single'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('change-password/', views.change_password, name='change_password'),
    path('student/add/', views.student_add_view, name='student_add'),
    path('student/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('student/list/', views.student_list, name='student_list'),
    path('validate-username/', views.validate_username, name='validate_username'),
]
