from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, QuesModel
from courses.models import Module

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'module', 'total_questions', 'total_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'course' in self.data:
            course_id = int(self.data.get('course'))
            self.fields['module'].queryset = Module.objects.filter(course=course_id)
        elif self.instance.pk:
            self.fields['module'].queryset = self.instance.course.module_set.all()
        else:
            self.fields['module'].queryset = Module.objects.none()

        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuesModel
        fields = ['question', 'op1', 'op2', 'op3', 'op4', 'ans']

QuestionFormSet = inlineformset_factory(Quiz, QuesModel, form=QuestionForm, extra=1)