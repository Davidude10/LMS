
from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
     path('courses/<int:course_id>/modules/', views.course_modules, name='course_modules'),
     path('course/module/<int:pk>/', views.module_details, name='module'),
     path('course_detail/', views.course_detail, name='course_detail'),
   path('courses/course_modules/', views.student_course, name='student_course'),
     path('new_course/', views.new_course, name='new_course'),
     path('new_module/<int:course_id>/', views.new_Module, name='new_Module'),
    
 
 
 
 
   path("chapter/<slug>/detail/", views.chapter_single, name="chapter_detail"),
    path("<int:pk>/chapter/add/", views.chapter_add, name="chapter_add"),
    path("chapter/<slug>/edit/", views.chapter_edit, name="edit_chapter"),
    path("chapter/delete/<slug>/", views.chapter_delete, name="delete_chapter"),
 
 
    path(
        "course/<slug>/documentations/upload/",
        views.handle_file_upload,
        name="upload_file_view",
    ),
    path(
        "course/<slug>/documentations/<int:file_id>/edit/",
        views.handle_file_edit,
        name="upload_file_edit",
    ),
    path(
        "course/<slug>/documentations/<int:file_id>/delete/",
        views.handle_file_delete,
        name="upload_file_delete",
    ),
    # Video uploads urls
    path(
        "course/<slug>/video_tutorials/upload/",
        views.handle_video_upload,
        name="upload_video",
    ),
    path(
        "course/<slug>/video_tutorials/<video_slug>/detail/",
        views.handle_video_single,
        name="video_single",
    ),
    path(
        "course/<slug>/video_tutorials/<video_slug>/edit/",
        views.handle_video_edit,
        name="upload_video_edit",
    ),
    path(
        "course/<slug>/video_tutorials/<video_slug>/delete/",
        views.handle_video_delete,
        name="upload_video_delete",
    ),
 
 
 
 
 
 
 
 
 
 
 
 
 
 ]
