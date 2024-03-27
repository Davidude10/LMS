from django.shortcuts import redirect, render, get_object_or_404
from .forms import QuizForm,QuestionForm
from .models import Quiz

from django.shortcuts import redirect, render
from .forms import QuizForm
from courses.models import Module,Course

def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            # Get the selected course from the form
            selected_course = quiz_form.cleaned_data['course']
            # Get the associated module for the selected course
            module = Module.objects.filter(course=selected_course).first()
            if module:
                quiz.module = module
                quiz.save()
                return redirect('quiz:create_questions', quiz_id=quiz.id)
            else:
                # Handle the case where no module is associated with the selected course
                # Redirect or display an error message as appropriate
                pass  # Placeholder, replace with your logic
    else:
        quiz_form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'quiz_form': quiz_form})


def create_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    total_questions = quiz.total_questions
    if request.method == 'POST':
        question_formset = QuestionForm(request.POST, instance=quiz)
        if question_formset.is_valid():
            question_formset.save()
            return redirect('home')  # Redirect to wherever appropriate
    else:
        question_formset = QuestionForm(instance=quiz)
    return render(request, 'quiz/create_questions.html', {'question_formset': question_formset, 'quiz': quiz  ,'total_questions': range(1,total_questions+1)})


def Assessment_detail(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            selected_course = quiz_form.cleaned_data['course']
            module = Module.objects.filter(course=selected_course).first()
            if module:
                quiz.module = module
                quiz.save()
                return redirect('quiz:create_questions', quiz_id=quiz.id)
            else:
                # Handle the case where no module is associated with the selected course
                # Redirect or display an error message as appropriate
                pass  # Placeholder, replace with your logic
    else:
        quiz_form = QuizForm()
    
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'quiz_form': quiz_form,
    }
    return render(request, "quiz/assessment_detail.html", context)