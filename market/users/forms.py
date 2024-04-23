from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile

__all__ = ["RegisterForm", "UserForm", "ProfileForm"]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ["email", "first_name"]
        labels = {
            "email": "Почта",
            "first_name": "Имя",
        }


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Profile
        fields = ["birthday", "image"]
        labels = {
            "birthday": "День рождения",
            "Картинка": "image",
        }
