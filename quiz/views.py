# views.py
from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question
from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Module

def create_quiz(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.module = module
            quiz.save()
            return redirect('quiz:add_questions', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'quiz_form': quiz_form, 'module': module})

def add_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz:add_choices', quiz_id=quiz_id, question_id=question.id)
    else:
        question_form = QuestionForm()
    return render(request, 'quiz/add_questions.html', {'question_form': question_form, 'quiz': quiz})

def add_choices(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.question = question
            choice.save()
            if question.choice_set.count() == 4:
                # Redirect to module details
                return redirect('courses:module', pk=quiz.module.id)
            else:
                return redirect('quiz:add_choices', quiz_id=quiz_id, question_id=question_id)
    else:
        choice_form = ChoiceForm()
    return render(request, 'quiz/add_choices.html', {'choice_form': choice_form, 'quiz': quiz, 'question': question})
