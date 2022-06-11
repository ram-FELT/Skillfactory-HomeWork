from django.db import models


class News(models.Model):

    dateCreation = models.DateTimeField(max_length=10, auto_now_add=True)

    Title = models.CharField(
        max_length=50,
        unique=True,
    )

    Text = models.TextField()

    def __str__(self):
        return f'{self.Title.title()}: {self.Text[:]}'

