from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django_filters.views import FilterView
from core.models import Session
from courses.models import Course
# from result.models import TakenCourse
from .decorators import admin_required
from .forms import StudentAddForm, ProfileUpdateForm
from .models import User, Student 
from .filters import  StudentFilter
from django.http import HttpResponse



from .models import Student
from .decorators import admin_required


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)


@login_required
def my_view(request):
    # Assuming the logged-in user is available through request.user
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        print(student.Course.title)
        return render(request, 'base.html', {'student': student})
    else:
        # Handle the case when the user is not logged in
        return render(request, 'base.html')

@login_required
def profile(request):
    current_session = Session.objects.filter(is_current_session=True).first()

    if request.user.is_authenticated:
        user_instance = User.objects.filter(pk=request.user.pk).first()

        if Student.objects.filter(user=user_instance).exists():
                courses = Course.objects.filter(
                    student__user=user_instance
                )
                context = {
                    "title": request.user.get_full_name,
                    "courses": courses,
                    "current_session": current_session,
                }
                return render(request, "users/profile.html", context)
        else:
                admin = User.objects.filter(is_admin=True)
                return render(
                    request,
                    "users/profile.html",
                    {
                        "title": request.user.get_full_name,
                        "admin": admin,
                        "current_session": current_session,
                    },
                )
    # Handle the case where the user is not authenticated or there's an issue with the user instance
    return HttpResponse("Unauthorized", status=401)
@login_required
@admin_required
def profile_single(request, pk):
    """Show profile of any selected user"""
    if request.user.id == pk:
        return redirect("/profile/")
    
    current_session = Session.objects.filter(is_current_session=True).first()


    user = User.objects.get(pk=pk)
    if user.is_student:
        student = Student.objects.get(id=pk)
        print(student.id)
        courses = Course.objects.filter(
            student=pk
        )
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "student",
            "courses": courses,
            "student": student,
            "current_session": current_session,
        }
        return render(request, "users/profile_single.html", context)
    else:
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "admin",
            "current_session": current_session,
        }
        return render(request, "users/profile_single.html", context)


@login_required
@admin_required
def admin_panel(request):
    return render(
        request, "setting/admin_panel.html", {"title": request.user.get_full_name}
    )

@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(
        request,
        "setting/profile_info_change.html",
        {
            "title": "Setting",
            "form": form,
        },
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error(s) below. ")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "setting/password_change.html",
        {
            "form": form,
        },
    )



##################################################################################################################


@login_required
@admin_required
def student_add_view(request):
    student=Student.objects.all()
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "users for " + first_name + " " + last_name + " has been created.",
            )
            return redirect("users:student_list")
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = StudentAddForm()

    return render(
        request,
        "users/add_student.html",
        {"title": "Add Student", "form": form ,"student":student},
    )


@login_required
@admin_required
def edit_student(request, pk):
    student = Student.objects.get(pk=pk)
    instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, ("Student " + full_name + " has been updated."))
            return redirect("users/student_list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(
        request,
        "users/edit_student.html",
        {
            "title": "Edit-profile",
            "form": form,
            "student":student,
        },
    )


@method_decorator([login_required, admin_required], name='dispatch')
class StudentListView(ListView):
    queryset = Student.objects.all()
    filterset_class = StudentFilter
    template_name = "users/student_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Students"
        return context


@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # full_name = student.user.get_full_name
    student.delete()
    messages.success(request, "Student has been deleted.")
    return redirect("student_list")


@login_required
@admin_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "users/student_list.html", {"students": students})
