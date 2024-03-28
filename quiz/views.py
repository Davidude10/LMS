
from .forms import QuizForm, QuestionForm, ChoiceForm
from courses.models import Course,Module,Chapter
from django.shortcuts import render,redirect

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


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz/Assessment_detail')  # Redirect to the quiz list page after adding the question
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})