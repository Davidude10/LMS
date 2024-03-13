# forms.py
from django import forms
from .models import Quiz, Question, Choice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'module', 'title']  # Add other fields as needed

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'mark']  # Add other fields as needed

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']  # Add other fields as needed
