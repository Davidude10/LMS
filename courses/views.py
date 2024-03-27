from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from courses.models import Chapter, Upload, UploadVideo
from .models import Course,Module
from .forms import CourseForm, ModuleForm,ChapterForm
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
    modules = course.module_set.all()

    # Adding chapter count for each module
    for module in modules:
        module.chapter_count = module.chapter_set.count()

    return render(request, 'courses/course_modules.html', {'course': course, 'modules': modules})
def new_Module(request, course_id):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course_id = course_id
            module.save()
            return redirect('courses:course_modules', course_id=course_id)  # Redirect to a success URL after adding the module
    else:
        form = ModuleForm()
    return render(request, 'courses/new_module.html', {'form': form})

def module_details(request, pk):
    module = Module.objects.get(id=pk)
    chapters = Chapter.objects.filter(module=module)
    

    context = {
        'module': module,
        'chapters': chapters,
    }

    return render(request, 'courses/module_details.html', context)


def add_chapter(request, module_id=None):
    module = None
    if module_id:
        module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter = form.save(commit=False)
            if module:
                chapter.module = module
            if 'file' in request.FILES:
                chapter.has_file = True
            if 'video' in request.FILES:
                chapter.has_video = True
            chapter.save()
            if module:
                return redirect('courses:module', pk=module.id)
            else:
                return redirect('display_chapter', chapter_id=chapter.id)
    else:
        form = ChapterForm()
    return render(request, 'courses/add_chapter.html', {'form': form, 'module': module})

def display_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    return render(request, 'display-chapter.html', {'chapter': chapter})