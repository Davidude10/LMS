from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
 
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()
            return redirect('quiz:create_questions', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'quiz_form': quiz_form})

def create_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        question_formset = QuestionFormSet(request.POST, instance=quiz)
        if question_formset.is_valid():
            question_formset.save()
            return redirect('courses:modules')
    else:
        question_formset = QuestionFormSet(instance=quiz)
    return render(request, 'quiz/create_questions.html', {'question_formset': question_formset})