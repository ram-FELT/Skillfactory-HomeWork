from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    category = models.CharField(max_length=64, verbose_name="Категория", unique=True)
    subscriber = models.ManyToManyField(User, through='Subscribe')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subscribe(models.Model):
    subscriber = models.ForeignKey(User, verbose_name="Имя подписчика", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)

    def __str__(self):
        return f'{User.objects.get(id=self.subscriber_id)} подписан на категорию {Category.objects.get(id=self.category_id)}'

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def get_absolute_url(self):
        return reverse('unsubscribe', args=[str(self.id)])


class News(models.Model):
    dateCreation = models.DateTimeField(max_length=10, auto_now_add=True)
    Title = models.CharField(max_length=50, unique=True,)
    Text = models.TextField()
    postType = models.CharField(max_length=16, verbose_name="Тип", choices=[('news', "Новость"), ('article', "Статья")],
                                default='article')
    PostCategory = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.contents[:123] + '...'

    def get_categories(self):
        return PostCategory.objects.filter(post=self)

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    news = models.ForeignKey(News, verbose_name="Пост", on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)

    def __str__(self):
        return f'{News.objects.get(id=self.news_id)} (Категория {Category.objects.get(id=self.Category_id)})'

    class Meta:
        verbose_name = "Связь"
        verbose_name_plural = "Связи"
