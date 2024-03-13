from django.contrib import admin
from django.contrib.auth.models import Group

from .models import TakenCourse, Result


class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "course",
        "assignment",
        
        "quiz",
        "total",
        
    ]


admin.site.register(TakenCourse, ScoreAdmin)
admin.site.register(Result)