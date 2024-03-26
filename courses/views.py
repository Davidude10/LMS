from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from courses.models import Chapter, Upload, UploadVideo
from .models import Course,Module
from .forms import CourseForm, ModuleForm
from django.shortcuts import render, get_object_or_404
from users.decorators import admin_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from users.models import Student
from django.template import loader

def course_detail(request):
    courses_count = Course.objects.count()
    modules_count = Module.objects.count()
    chapters_count = Chapter.objects.count()
    courses=Course.objects.all()

    context = {
        'courses_count': courses_count,
        'modules_count': modules_count,
        'chapters_count': chapters_count,
        'courses':courses,
    }
    return render(request,"courses/course_detail.html",context)
    
@admin_required
@login_required
def new_course(request):
    if request.method != 'POST':
        form = CourseForm()
    else:
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.owner = request.user
            new_course.save()
            return HttpResponseRedirect(reverse('courses:course_detail'))

    context = {'form': form}
    return render(request, 'courses/new_course.html', context)



def course_modules(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    modules = course.module_set.all()  # Assuming 'Module' is related name in 'Course' model
    return render(request, 'courses/course_modules.html', {'course': course, 'modules': modules})

def new_Module(request, course_id):
    # Retrieve the course object based on the course_id
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            # Set the course instance before saving the module
            module = form.save(commit=False)
            module.course = course
            module.save()
            return HttpResponseRedirect('courses:course_modules')  # Redirect to a success URL after adding the module
    else:
        form = ModuleForm()
    
    return render(request, 'courses/new_Module.html', {'form': form})