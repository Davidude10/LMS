
from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
#     path('', views.courses, name='courses'),
#     path('course/<int:pk>/', views.course_details, name='course'),
#     path('course/module/<int:pk>/', views.module_details, name='module'),
     path('course_detail/', views.course_detail, name='course_detail'),
#     path('course/<int:pk>/info/', views.course_infos, name='course_infos'),
#     path('course_info/', views.course_info, name='course_info'),
     path('new_course/', views.new_course, name='new_course'),
#     path('new_module/<int:course_id>/', views.new_Module, name='new_Module'),
#     path('edit_Module/<int:Module_id>/', views.edit_Module, name='edit_Module'),
#     path('delete_Module/<int:Module_id>/', views.delete_Module, name='delete_Module'),
#     path('Course/list/', views.Course_list, name='course_list'),
 ]
