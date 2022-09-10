from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
from random import random



class Author(models.Model):
    author = models.OneToOneField(User, verbose_name="Автор", on_delete=models.CASCADE)
    otc = models.CharField(max_length=64)

    def make_code(self):
        code = (str(random())[2:8]) + 'at' + str(datetime.timestamp(datetime.now()))[:10]
        self.otc = code
        self.save()
        return code

    def __str__(self):
        return f' {self.author.username} (#{self.pk})'


class Post(models.Model):
    TYPE = [('tank', "Танки"),
            ('heal', "Хилы"),
            ('dd', "ДД"),
            ('trade', "Торговцы"),
            ('guildmaster', "Гилдмастеры"),
            ('questgiver', "Квестгиверы"),
            ('smith', "Кузнецы"),
            ('tanner', "Кожевники"),
            ('potionmaster', "Зельевары"),
            ('spellmaster', "Мастера заклинаний")]

    author = models.ForeignKey(Author, verbose_name="Автор объявления", on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    contents = models.TextField(verbose_name="Текст")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.CharField(max_length=32, verbose_name="Категория", choices=TYPE, default='tank')
    upload = models.FileField(blank=True, upload_to='uploads/', verbose_name="Загруженный файл")

    def __str__(self):
        return f'{self.title[:16]}, "{self.contents[:16]}" ({self.type}) - {self.creation_date.strftime("%d.%m.%Y, %H:%M:%S")}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def count_comments(self):
        return len(self.comments.all())

    @property
    def type(self):
        for s in self.TYPE:
            if self.category in s:
                return s[1]


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name="Объявление", on_delete=models.CASCADE, related_name='comments')
    commentator = models.ForeignKey(User, verbose_name="Откликнувшийся пользователь", on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    contents = models.TextField(verbose_name="Текст отклика")
    accepted = models.BooleanField(default=False, verbose_name="Принят")

    def __str__(self):
        return f'{self.post} <- {self.contents[:32]}... - {self.creation_date.strftime("%d.%m.%Y, %H:%M:%S")}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.pk)])

'''
class UserDoc(models.Model):
    img = models.ImageField(upload_to='images_uploaded', null=True)
    video = models.FileField(upload_to='videos_uploaded', null=True,
                             validators=[
                                 FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
'''