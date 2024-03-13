

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager,Group,Permission
from .validators import ASCIIUsernameValidator
from django.db.models import Q
from django.urls import reverse
from PIL import Image
from courses.models import Course


GENDERS = (("M", "Male"), ("F", "Female"))

class CustomUserManager(UserManager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(or_lookup).distinct()
        return queryset
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to="profile_pictures/%Y/%m/%d/", default="default.png", null=True)
    email = models.EmailField(blank=True, null=True)
    groups = models.ManyToManyField(
        Group, related_name='custom_user_groups', blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions', blank=True,
        help_text="Specific permissions for this user.",
    )

    username_validator = ASCIIUsernameValidator()

    objects = CustomUserManager()

    

    class Meta:
        ordering = ("-date_joined",)

    def get_courses(self):
        return Course.get_user_courses(self)

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
        return full_name
    
    @property
    def get_user_role(self):
        if self.is_superuser:
            return "Admin"
        elif self.is_student:
            return "Student"
        return ""

    def get_picture(self):
        try:
            return self.picture.url
        except:
            return settings.MEDIA_URL + "default.png"

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture and self.picture.url != settings.MEDIA_URL + "default.png":
            self.picture.delete()
        super().delete(*args, **kwargs)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return self.user.get_full_name

    @classmethod
    def get_gender_count(cls):
        males_count = Student.objects.filter(user__gender="M").count()
        females_count = Student.objects.filter(user__gender="F").count()
        return {"M": males_count, "F": females_count}

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
