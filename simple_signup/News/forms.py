from django import forms
from django.core.exceptions import ValidationError
from .models import News, Subscribe
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'Title',
            'Text',
            'postType',
            'PostCategory',

        ]

    def clean(self):
        cleaned_data = super().clean()
        Text = cleaned_data.get("Text")
        Title = cleaned_data.get("Title")

        if Title == Text:
            raise ValidationError(
                "Текст не должно быть идентичен оглавлению."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, *args, **kwargs):
        user = super(BasicSignupForm, self).save(*args, **kwargs)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = [
            'category',
        ]
