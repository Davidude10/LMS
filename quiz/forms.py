from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import User
from .models import QuesModel

class addQuestionform(ModelForm):
    class Meta:
        model=QuesModel
        fields="__all__"