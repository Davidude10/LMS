from django import forms
from .models import Quiz, Question, Choice, QuizAttempt
from courses.models import Course, Module
from django.contrib.auth import get_user_model


class QuizForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Course"
    )
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Module"
    )
    total_questions = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Total Questions"
    )
    total_score = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Total Score"
    )

    class Meta:
        model = Quiz
        fields = ['course', 'module', 'total_questions', 'total_score']

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Question Text"}),
        label="Question Text",
    )

    class Meta:
        model = Question
        fields = ['question_text']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['question_text'].widget.attrs['class'] = 'form-control'

    # Define inline formset for choices
    ChoiceFormSet = forms.inlineformset_factory(
        Question,
        Choice,
        fields=('choice_text', 'is_correct'),
        extra=4,  # Number of extra choice forms to display
        can_delete=False
    )

class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Choice Text"}),
        label="Choice Text",
    )
    is_correct = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Is Correct",
        required=False,
    )

    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']

class QuizAttemptForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Student"
    )
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Score"
    )

    class Meta:
        model = QuizAttempt
        fields = ['student', 'score']
