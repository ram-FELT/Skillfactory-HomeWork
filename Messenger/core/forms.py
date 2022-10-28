from django.contrib.auth.forms import UserCreationForm

from room.models import ChatUser
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = ChatUser
        fields = [
            'username',
            'password1',
            'password2'
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = ChatUser
        fields = ('avatar', 'username',)
        help_texts = {
            'username': None
        }