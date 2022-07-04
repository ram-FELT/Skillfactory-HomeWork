from django.db import models
from django.urls import reverse


class News(models.Model):
    dateCreation = models.DateTimeField(max_length=10, auto_now_add=True)
    Title = models.CharField(
        max_length=50,
        unique=True,
    )
    Text = models.TextField()
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='News',
    )

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class Category(models.Model):
    NEWS = 'Новость'
    ARTICLE = 'Статья'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    name = models.CharField(max_length=7, choices=CATEGORY_CHOICES, default=ARTICLE)

    def __str__(self):
        return self.name.title()
