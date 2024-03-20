from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django import forms
from django.db import transaction
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth.forms import PasswordResetForm
from courses.models import Course
from .models import User, Student,GENDERS
import random
import string



class StudentAddForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First name",
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last name",
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Course",
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

   

    

    

    

    

    

    
    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'course','email', 'phone', 'address', 'phone']

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.gender = self.cleaned_data.get("gender")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")

        # Generate a username based on first and last name and registration date
        registration_date = int(datetime.now().strftime("%Y")) % 2000

        total_students_count = Student.objects.count()
        random_alphabets = ''.join(random.choices(string.ascii_uppercase, k=4))
        random_numbers = ''.join(random.choices(string.digits, k=4))
        random_string = random_alphabets + random_numbers

        generated_username = (
            f"ST-{registration_date}-{total_students_count}"
        )
        # Generate a password
        generated_password = (
            f"{random_string}"
        )

        user.username = generated_username
        user.set_password(generated_password)

        if commit:
            user.save()
            Student.objects.create(
                user=user,
                course=self.cleaned_data.get("course"),
            )

            # Send email with the generated credentials
            send_mail(
                "Your Mentorow LMS account credentials",
                f"Your ID: {generated_username}\nYour password: {generated_password}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        return user


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First Name",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last Name",
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Phone No.",
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address / city",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "phone",
            "address",
            "picture",
        ]


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-mail address. "
            self.add_error("email", msg)
            return email
