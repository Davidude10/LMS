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
from quiz.models import Quiz

@login_required
def courses(request):
    """Request a page which displays all the courses."""
    courses = Course.objects.order_by('date_added')
    
    context = {'courses': courses}
    return render(request, 'courses/courses.html', context)

@login_required
def course_details(request, pk):
    """Show details of courses for the logged-in user."""
    course = get_object_or_404(Course, pk=pk)
    modules = Module.objects.filter(course=course)
    chapters = Chapter.objects.filter(module__in=modules)
    chapter_count=Chapter.get_chapter_count()

    context = {'course': course, 'modules': modules, 'chapters': chapters,'chapter_count': chapter_count}
    return render(request, 'courses/course_details.html', context)

@login_required
def module_details(request, pk):
    """Show details of courses for the logged-in user."""
    course = get_object_or_404(Course, pk=pk)
    module = Module.objects.filter(course_id=course.id).first()  # Retrieve the first module
    if module:
        chapters = Chapter.objects.filter(module_id=module.id)
        quiz=Quiz.objects.filter(module_id=module.id)
        chapter_count = Chapter.get_chapter_count()
    else:
        chapters = []
        chapter_count = 0
    
    context = {'course': course, 'module': module, 'chapters': chapters, 'chapter_count': chapter_count,'quiz':quiz}
    return render(request, 'courses/module_details.html', context)

@login_required
def course_infos(request, pk):
    """Show details of courses for the logged-in user."""
    course = get_object_or_404(Course, pk=pk)
    modules = Module.objects.filter(course=course)
    chapters = Chapter.objects.filter(module__in=modules)
    chapter_count=Chapter.get_chapter_count()

    context = {'course': course, 'modules': modules, 'chapters': chapters,'chapter_count': chapter_count}
    return render(request, 'courses/course_infos.html', context)

@login_required
def course_detail(request):
    """Show details of the course for the logged-in user."""
    # Assuming the logged-in user is a student
    student = get_object_or_404(Student, user=request.user)
    enrolled_course = student.course
    if enrolled_course:
        modules = Module.objects.filter(course=enrolled_course)
        chapters = Chapter.objects.filter(module__in=modules)
        chapter_count = Chapter.get_chapter_count()

        context = {'course': enrolled_course, 'modules': modules, 'chapters': chapters, 'chapter_count': chapter_count}
        return render(request, 'courses/course_detail.html', context)
    else:
        # Handle the case where the student is not enrolled in any course
        # You can redirect to another page or show an error message
        return HttpResponse("You are not enrolled in any course.")

@login_required
def course_info(request):
    """Show details of the course for the logged-in user."""
    # Assuming the logged-in user is a student
    student = get_object_or_404(Student, user=request.user)
    enrolled_course = student.course
    if enrolled_course:
        modules = Module.objects.filter(course=enrolled_course)
        chapters = Chapter.objects.filter(module__in=modules)
        chapter_count = Chapter.get_chapter_count()

        context = {'course': enrolled_course, 'modules': modules, 'chapters': chapters, 'chapter_count': chapter_count}
        return render(request, 'courses/course_info.html', context)
    else:
        # Handle the case where the student is not enrolled in any course
        # You can redirect to another page or show an error message
        return HttpResponse("You are not enrolled in any course.")

@login_required
def new_course(request):
    """Add a new course."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CourseForm()
    else:
        # POST data submitted; process data.
        form = CourseForm(request.POST)
        # Set the queryset for the owner field
        
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.owner = request.user
            new_course.save()
            return HttpResponseRedirect(reverse('courses:courses'))

    context = {'form': form}
    return render(request, 'courses/new_course.html', context)


@login_required
def new_Module(request, course_id):
    """Add a new Module for a particular course."""
    course = Course.objects.get(id=course_id)

    if request.method != 'POST':
        form = ModuleForm()
    else:
        form = ModuleForm(data=request.POST)
        if form.is_valid():
            new_Module = form.save(commit=False)
            new_Module.course = course
            new_Module.save()
            return HttpResponseRedirect(reverse('courses:course', args=[course_id]))

    context = {'course': course, 'form': form}
    return render(request, 'courses/new_Module.html', context)


@login_required
def edit_Module(request, Module_id):
    """Edit an Module made by the user."""
    Module = Module.objects.get(id=Module_id)
    course = Module.course

    if request.method != 'POST':
        # Initial request; pre-fill for with the current Module.
        form = ModuleForm(instance=Module)
    else:
        # POST data submitted; process data.
        form = ModuleForm(instance=Module, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('courses:course',args=[course.id]))

    context = {'Module': Module, 'course': course, 'form': form}
    return render(request, 'edit_Module.html', context)

@login_required
def delete_Module(request, Module_id):
    """Delete an Module made by the user."""
    Module = Module.objects.get(id=Module_id)
    course = Module.course
    Module.delete()

    return HttpResponseRedirect(reverse('courses:course', args=[course.id]))







def chapter_redirect_view(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    # Check if the chapter has an associated file
    if chapter.upload_set.exists():
        file = chapter.upload_set.first()
        return redirect(file.file.url)
    # Check if the chapter has an associated video
    elif chapter.uploadvideo_set.exists():
        video = chapter.uploadvideo_set.first()
        return redirect(video.video.url)
    # Handle the case where there is no file or video associated with the chapter
    else:
        # You can redirect to a 404 page or any other appropriate action
        return redirect('404_page')


@login_required
@admin_required
def Course_list(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, "courses/courses.html", {"courses": courses})
