from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from courses.models import Chapter, Upload, UploadVideo
from .models import Course,Module
from .forms import CourseForm, ModuleForm,ChapterAddForm
from django.shortcuts import render, get_object_or_404
from users.decorators import admin_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from users.models import Student,User
from django.template import loader
from courses.forms import UploadFormFile,UploadFormVideo
from django.contrib import messages

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
    chapter = Chapter.objects.filter(module_id=pk)
    

    context = {
        'module': module,
        'chapter': chapter,
    }

    return render(request, 'courses/module_details.html', context)


# def add_chapter(request, module_id=None):
#     module = None
#     if module_id:
#         module = get_object_or_404(Module, id=module_id)
#     if request.method == 'POST':
#         form = ChapterForm(request.POST, request.FILES)
#         if form.is_valid():
#             chapter = form.save(commit=False)
#             if module:
#                 chapter.module = module
#             if 'file' in request.FILES:
#                 chapter.has_file = True
#             if 'video' in request.FILES:
#                 chapter.has_video = True
#             chapter.save()
#             if module:
#                 return redirect('courses:module', pk=module.id)
#             else:
#                 return redirect('display_chapter', chapter_id=chapter.id)
#     else:
#         form = ChapterForm()
#     return render(request, 'courses/add_chapter.html', {'form': form, 'module': module})

# def display_chapter(request, chapter_id):
#     chapter = get_object_or_404(Chapter, pk=chapter_id)
#     return render(request, 'display-chapter.html', {'chapter': chapter})





# ########################################################
# File Upload views
# ########################################################
@login_required
@admin_required
def handle_file_upload(request, slug):
    chapter = Chapter.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.chapter = chapter
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("courses:chapter_detail", slug=slug)
    else:
        form = UploadFormFile()
    return render(
        request,
        "upload/upload_file_form.html",
        {"title": "File Upload", "form": form, "chapter": chapter},
    )


@login_required
@admin_required
def handle_file_edit(request, slug, file_id):
    chapter = Chapter.objects.get(slug=slug)
    instance = Upload.objects.get(pk=file_id)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        # file_name = request.POST.get('name')
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("courses:chapter_detail", slug=slug)
    else:
        form = UploadFormFile(instance=instance)

    return render(
        request,
        "upload/upload_file_form.html",
        {"title": instance.title, "form": form, "course":chapter},
    )


def handle_file_delete(request, slug, file_id):
    file = Upload.objects.get(pk=file_id)
    # file_name = file.name
    file.delete()

    messages.success(request, (file.title + " has been deleted."))
    return redirect("courses:chapter_detail", slug=slug)


# ########################################################
# Video Upload views
# ########################################################
@login_required
@admin_required
def handle_video_upload(request, slug):
    chapter = Chapter.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.chapter = chapter
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("courses:chapter_detail", slug=slug)
    else:
        form = UploadFormVideo()
    return render(
        request,
        "upload/upload_video_form.html",
        {"title": "Video Upload", "form": form, "chapter": chapter},
    )


@login_required
# @admin_required
def handle_video_single(request, slug, video_slug):
    chapter = get_object_or_404(Chapter, slug=slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    return render(request, "upload/video_single.html", {"video": video  , "chapter":chapter})


@login_required
@admin_required
def handle_video_edit(request, slug, video_slug):
    chapter = Chapter.objects.get(slug=slug)
    instance = UploadVideo.objects.get(slug=video_slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("courses:chapter_detail", slug=slug)
    else:
        form = UploadFormVideo(instance=instance)

    return render(
        request,
        "upload/upload_video_form.html",
        {"title": instance.title, "form": form, "chapter": chapter},
    )


def handle_video_delete(request, slug, video_slug):
    video = get_object_or_404(UploadVideo, slug=video_slug)
    # video = UploadVideo.objects.get(slug=video_slug)
    video.delete()

    messages.success(request, (video.title + " has been deleted."))
    return redirect("courses:chapter_detail", slug=slug)




# ########################################################
# Chapter views
# ########################################################
@login_required
def chapter_single(request, slug):
    chapter = Chapter.objects.get(slug=slug)
    files = Upload.objects.filter(chapter__slug=slug)
    videos = UploadVideo.objects.filter(chapter__slug=slug)


    return render(
        request,
        "courses/chapter_single.html",
        {
            "title": chapter.title,
            "chapter": chapter,
            "files": files,
            "videos": videos,
            "media_url": settings.MEDIA_ROOT,
        },
    )


@login_required
@admin_required
def chapter_add(request, pk):
    users = User.objects.all()
    if request.method == "POST":
        form = ChapterAddForm(request.POST)
        chapter_name = request.POST.get("title")
        
        if form.is_valid():
            form.save()
            messages.success(
                request, (chapter_name + " has been created.")
            )
            return redirect("courses:module", pk=request.POST.get("module"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = ChapterAddForm(initial={"module": Module.objects.get(pk=pk)})

    return render(
        request,
        "courses/chapter_add.html",
        {
            "title": "Add Chapter",
            "form": form,
            "module": pk,
            "users": users,
        },
    )


@login_required
@admin_required
def chapter_edit(request, slug):
    chapter = get_object_or_404(Chapter, slug=slug)
    if request.method == "POST":
        form = ChapterAddForm(request.POST)
        chapter_name = request.POST.get("title")
        
        if form.is_valid():
            form.save()
            messages.success(
                request, (chapter_name + " has been edited.")
            )
            return redirect("courses:module_detail", pk=request.POST.get("module"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = ChapterAddForm(instance=chapter)

    return render(
        request,
        "courses/chapter_add.html",
        {
            "title": "Edit Chapter",
            # 'form': form, 'program': pk, 'course': pk
            "form": form,
        },
    )


@login_required
@admin_required
def chapter_delete(request, slug):
    chapter = Chapter.objects.get(slug=slug)
    # course_name = course.title
    chapter.delete()
    messages.success(request, "Chapter " + chapter.title + " has been deleted.")

    return redirect("courses:module_detail", pk=chapter.module.id)
@login_required
def student_course(request):
    # Get the course assigned to the current user
    user_course = request.user.student.course
    
    # Get the modules related to the user's course
    modules = Module.objects.filter(course=user_course)
    
    # Pass the modules to the template context
    context = {'modules': modules}
    
    return render(request, "courses/course_modules.html", context)