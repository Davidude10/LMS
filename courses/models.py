from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .utils import unique_slug_generator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from core.models import ActivityLog
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

class CourseManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(code__icontains=query)
                | Q(slug__icontains=query)
            )
            queryset = queryset.filter(or_lookup).distinct()
        return queryset

class Course(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(null=True, default=0)
    image=models.ImageField(upload_to="course_icon/%Y/%m/%d/", default="default.png", null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(null=True, blank=True)
    objects = CourseManager()

    def __str__(self):
        return self.title

@receiver(post_save, sender=Course)
def log_save_program(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The program '{instance}' has been {verb}.")

@receiver(post_delete, sender=Course)
def log_delete_program(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The program '{instance}' has been deleted.")

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200, unique=False, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    module_no=models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Module"
        unique_together = ('course', 'title')

    def __str__(self):
        return self.title
    
    def clean(self):
        # Ensure each module is unique to each course
        if Module.objects.filter(course=self.course, title=self.title).exists():
            raise ValidationError(_('Module with this title already exists for this course.'))

class Chapter(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=200, blank=True, null=True)
    chapter_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:chapter_detail", kwargs={"slug": self.slug})

def chapter_pre_save_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(chapter_pre_save_receiver, sender=Chapter)

@receiver(post_save, sender=Chapter)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The chapter '{instance}' has been {verb}.")

@receiver(post_delete, sender=Chapter)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The chapter '{instance}' has been deleted.")

class Upload(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="chapter_files/",
        help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
        validators=[
            FileExtensionValidator(
                [
                    "pdf",
                    "docx",
                    "doc",
                    "xls",
                    "xlsx",
                    "ppt",
                    "pptx",
                    "zip",
                    "rar",
                    "7zip",
                ]
            )
        ],
    )
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext) - 1]

        if ext in ("doc", "docx"):
            return "word"
        elif ext == "pdf":
            return "pdf"
        elif ext in ("xls", "xlsx"):
            return "excel"
        elif ext in ("ppt", "pptx"):
            return "powerpoint"
        elif ext in ("zip", "rar", "7zip"):
            return "archive"

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

@receiver(post_save, sender=Upload)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The file '{instance.title}' has been uploaded to the chapter '{instance.chapter}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The file '{instance.title}' of the chapter '{instance.chapter}' has been updated."
        )

@receiver(post_delete, sender=Upload)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The file '{instance.title}' of the chapter '{instance.chapter}' has been deleted."
    )

class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to="chapter_videos/",
        help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
    )
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse(
            "courses:video_single", kwargs={"slug": self.chapter.slug, "video_slug": self.slug}
        )

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)

def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(video_pre_save_receiver, sender=UploadVideo)

@receiver(post_save, sender=UploadVideo)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The video '{instance.title}' has been uploaded to the chapter {instance.chapter}."
        )
    else:
        ActivityLog.objects.create(
            message=f"The video '{instance.title}' of the chapter '{instance.chapter}' has been updated."
        )

@receiver(post_delete, sender=UploadVideo)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The video '{instance.title}' of the chapter '{instance.chapter}' has been deleted."
    )