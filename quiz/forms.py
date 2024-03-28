# quiz/forms.py

from django import forms
from .models import Question,Quiz,Choice,QuizAttempt
from courses.models import Course, Module

class QuizForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), disabled=True)
    module = forms.ModelChoiceField(queryset=Module.objects.none())

    class Meta:
        model = Quiz
        fields = ['course', 'module']

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        if 'course' in kwargs:
            course = kwargs.pop('course')
            self.fields['module'].queryset = Module.objects.filter(course=course)

class QuestionForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), disabled=True)
    module = forms.ModelChoiceField(queryset=Module.objects.none())

    class Meta:
        model = Question
        fields = ['course', 'module', 'text', 'correct_answer']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if 'course' in kwargs:
            course = kwargs.pop('course')
            self.fields['module'].queryset = Module.objects.filter(course=course)

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']

class QuizAttemptForm(forms.ModelForm):
    class Meta:
        model = QuizAttempt
        fields = []

    def __init__(self, *args, **kwargs):
        super(QuizAttemptForm, self).__init__(*args, **kwargs)
        choices = Choice.objects.filter(question=self.instance.quiz.question_set.first())
        for choice in choices:
            self.fields[f'choice_{choice.pk}'] = forms.BooleanField(label=choice.text, required=False)

    def clean(self):
        cleaned_data = super().clean()
        choices = Choice.objects.filter(question=self.instance.quiz.question_set.first())
        selected_choices = [key for key, value in cleaned_data.items() if key.startswith('choice_') and value]
        correct_choices = [choice.pk for choice in choices if choice.text == choice.question.correct_answer]
        if sorted(selected_choices) == sorted(correct_choices):
            self.instance.score = 1  # Setting score to 1 if all correct choices are selected
        else:
            self.instance.score = 0  # Setting score to 0 if any incorrect choice is selected