from django.contrib import admin

from courses.models import Course
from courses.models import Module,Chapter

from .forms import ChapterForm

class ChapterAdmin(admin.ModelAdmin):
    form = ChapterForm
    
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Chapter, ChapterAdmin)


