
from .forms import QuizForm, QuestionForm
from courses.models import Course,Module

from django.shortcuts import render,redirect
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory


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
    quizzes=Quiz.objects.all()
    context = {
        'courses': courses,
        'Quiz':quizzes,
        'quiz_form': quiz_form,
    }
    return render(request, "quiz/assessment_detail.html", context)


@login_required
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz/quiz.html", {'quiz':quiz})

def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, myid):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Choice.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})
     
        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})
    

def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            obj = form.instance
            return redirect('quiz:Assessment_detail')
        else:
            # Form is not valid, render the form again with validation errors
            return render(request, "quiz/add_quiz.html", {'form': form})
    else:
        form = QuizForm()  # Initialize form without passing any instance
    return render(request, "quiz/add_quiz.html", {'form': form})

def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:add_question')
    else:
        form=QuestionForm()
    return render(request, "quiz/add_question.html", {'form':form, 'questions':questions})

def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('quiz/add_question')
    return render(request, "quiz/delete_question.html", {'question':question})


def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Choice, fields=('Choice','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "quiz/add_options.html", {'alert':alert})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "quiz/add_options.html", {'formset':formset, 'question':question})