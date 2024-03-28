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
    image=forms.ImageField(widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Image",)
    summary = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Summary"}),
        label="Summary",
        required=False,
    )
  
    class Meta:
        model = Course
        fields = ['title', 'duration','image' ,'summary']

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

class ChapterAddForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['module','title','summary']
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        
        

    # Upload files to specific course
class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = (
            "title",
            "file",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["file"].widget.attrs.update({"class": "form-control"})


# Upload video to specific course
class UploadFormVideo(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = (
            "title",
            "video",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["video"].widget.attrs.update({"class": "form-control"})