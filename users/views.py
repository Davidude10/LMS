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


##################################################################################################################

@login_required
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'users/student_profile.html', {'student': student})












##########################################################################################################################


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
def edit_student(request, id):
    student = Student.objects.get(id=id)
    instance=get_object_or_404(Student,id=id)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            form.save()

            
            return redirect("users:student_list")
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
    student = get_object_or_404(Student, id=pk)
    # full_name = student.user.get_full_name
    student.delete()
    messages.success(request, "Student has been deleted.")
    return redirect("users:student_list")


@login_required
@admin_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "users/student_list.html", {"students": students})