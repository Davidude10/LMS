from django import forms
from .models import Course, Module, Chapter,Upload,UploadVideo

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
        label="Title",
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Duration (Months)"}),
        label="Duration (Months)",
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Summary"}),
        label="Summary",
        required=False,
    )
  
    class Meta:
        model = Course
        fields = ['title', 'duration', 'summary']

class ModuleForm(forms.ModelForm):
    course=forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Course",
    )

    title=forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
        label="Title",
    )

    module_no=forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Module number"}),
        label="Module number",
    )

    
    class Meta:
        model = Module
        fields = ['course', 'title', 'module_no']
        labels = {'course': ''}

class ChapterForm(forms.ModelForm):
    file = forms.FileField(label='Upload File', required=False)
    video = forms.FileField(label='Upload Video', required=False)

    class Meta:
        model = Chapter
        fields = ['module','title', 'chapter_number']

    def save(self, commit=True):
        # Get the Chapter instance
        chapter = super().save(commit=commit)

        # Save related objects if Chapter instance is fully saved
        if commit:
            file = self.cleaned_data.get('file')
            video = self.cleaned_data.get('video')

            if file:
                upload = Upload.objects.create(title=f'File for Chapter {chapter.chapter_number}', chapter=chapter, file=file)
                # You may want to do additional processing here

            if video:
                upload_video = UploadVideo.objects.create(title=f'Video for Chapter {chapter.chapter_number}', chapter=chapter, video=video)
                # You may want to do additional processing here

        return chapter