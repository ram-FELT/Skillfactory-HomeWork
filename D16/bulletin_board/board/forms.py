from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class BaseRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, label="Псевдоним в системе")
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=False, label="Имя", help_text="необязательно")
    last_name = forms.CharField(required=False, label="Фамилия", help_text="необязательно")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'contents',
            'category',
            'upload',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('contents',)
