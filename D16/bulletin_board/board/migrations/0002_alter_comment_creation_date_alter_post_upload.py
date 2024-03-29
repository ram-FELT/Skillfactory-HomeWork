# Generated by Django 4.1 on 2022-09-01 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='upload',
            field=models.FileField(blank=True, upload_to='uploads/', verbose_name='Загруженный файл'),
        ),
    ]
