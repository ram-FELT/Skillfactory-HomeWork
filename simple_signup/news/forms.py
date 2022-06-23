from django import forms
from django.core.exceptions import ValidationError
from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
           'Title',
           'Text',
           'category',
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
