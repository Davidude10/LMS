from django import forms
from .models import Quiz, Question
from django.contrib import admin
from courses.models import Course,Module

class QuizForm(forms.ModelForm):

    Quiz_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Quiz Name",
    )
    
    Course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)
    Module = forms.ModelChoiceField(queryset=Module.objects.none(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        if 'Course' in self.data:
            try:
                course_id = int(self.data.get('Course'))
                print(course_id)
                self.fields['Module'].queryset = Module.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                print(False)
        elif self.instance and self.instance.Course:
            self.fields['Module'].queryset = self.instance.Course.module_set.all()

    number_of_questions = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "type": "number",
                "class": "form-control",
            }
        ),
        label="Number of Questions",
    )
    
    time = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Time",
    )

    class Meta:
        model = Quiz
        fields = ('Quiz_name','Course','Module', 'number_of_questions', 'time')

    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('Question', 'quiz')
        
