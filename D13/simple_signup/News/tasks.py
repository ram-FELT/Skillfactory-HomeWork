from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import News, Category, Subscribe, PostCategory
import datetime


@shared_task
def mailing_list(title, text):
    instance = News.objects.get(Title=title, Text=text)
    for cat in instance.PostCategory.all():
        for subscribe in Subscribe.objects.filter(category=cat):
            msg = EmailMultiAlternatives(
                subject=instance.Title,
                body=instance.Text,
                from_email='Ev5hap@yandex.ru',
                to=[subscribe.subscriber.email],
            )
            html_content = render_to_string(
                'subscribeletter.html',
                {
                    'new': instance,
                    'recipient': subscribe.subscriber
                }
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

            print('Уведомление отослано подписчику ', subscribe.subscriber, ' на тему ', subscribe.category)


@shared_task
def weekly_mailing_list():
    for post in News.objects.filter(dateCreation__gt=(datetime.date.today()-datetime.timedelta(days=7))):
        for cat in PostCategory.objects.filter(news=post):
            for subscribe in Subscribe.objects.filter(category=cat.Category):
                msg = EmailMultiAlternatives(
                    subject=post.Title,
                    body=post.Text,
                    from_email='Ev5hap@yandex.ru',
                    to=[subscribe.subscriber.email],
                )
                html_content = render_to_string(
                    'weeklysubscribeletter.html',
                    {
                        'new': post,
                        'recipient': subscribe.subscriber
                    }
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                print('Уведомление отослано подписчику ', subscribe.subscriber, ' на тему ', subscribe.category)

