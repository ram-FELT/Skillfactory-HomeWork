from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .apscheduler import itstime
from .models import *
import datetime


@receiver(m2m_changed, sender=PostCategory)
def mailing_list(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance)
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


@receiver(itstime, sender='Weekly')
def mailing_list2(sender, **kwargs):
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
