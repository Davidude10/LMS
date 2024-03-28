from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.decorators import admin_required,student_required
from users.models import User, Student
from .forms import SessionForm ,NewsAndEventsForm
from .models import NewsAndEvents, Session

from courses.models import Course,Module,Chapter


# ########################################################
# News & Events
# ########################################################
@login_required
def home_view(request):
    items = NewsAndEvents.objects.all().order_by("-updated_date")

    module=Module.objects.all()
    chapter=Chapter.objects.all()
    

    context = {
        "title": "News & Events",
        "items": items,
        "module":module,
        "chapter":chapter,
        
        "current_session": Session.objects.filter(is_current_session=True).first(),  # Add current session to context
    }
    return render(request, "core/index.html", context)

@login_required
def post_add(request):
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been uploaded."))
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm()
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Add Post",
            "form": form,
        },
    )


@login_required
@admin_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been updated."))
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Edit Post",
            "form": form,
        },
    )


@login_required
@admin_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + " has been deleted."))
    return redirect("home")


@login_required
@admin_required
def session_list_view(request):
    """Show list of all sessions"""
    sessions = Session.objects.all().order_by("-is_current_session", "-session")
    return render(request, "core/session_list.html", {"sessions": sessions})


@login_required
@admin_required
def session_add_view(request):
    """check request method, if POST we add session otherwise show empty form"""
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_session"
            )  # returns string of 'True' if the user selected Yes
            print(data)
            if data == "true":
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, "Session added successfully. ")
            return redirect("session_list")

    else:
        form = SessionForm()
    return render(request, "core/session_update.html", {"form": form})


@login_required
@admin_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        data = form.data.get("is_current_session")
        if data == "true":
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()

            if form.is_valid():
                form.save()
                messages.success(request, "Session updated successfully. ")
                return redirect("session_list")
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, "Session updated successfully. ")
                return redirect("session_list")

    else:
        form = SessionForm(instance=session)
    return render(request, "core/session_update.html", {"form": form})


@login_required
@admin_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if session.is_current_session:
        messages.error(request, "You cannot delete current session")
        return redirect("session_list")
    else:
        session.delete()
        messages.success(request, "Session successfully deleted")
    return redirect("session_list")