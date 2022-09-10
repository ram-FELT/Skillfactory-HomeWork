from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Author, User, Comment, Post
from django.conf import settings
from .apscheduler import go_mail
from django.template.loader import render_to_string
import datetime


@receiver(post_save, sender=User)
def registration_mail(sender, instance, **kwargs):
    if not instance.is_active:
        author = Author.objects.create(author=instance)
        code = author.make_code()[:6]
        print(code)
        send_mail(
            "Подтверждение регистрации на портале",
            ("Для подтверждения регистрации введите код " + code + ", Время действия кода - 1 час"),
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )


@receiver(post_save, sender=Comment)
def comment_mail(sender, instance, **kwargs):
    # коммент принят
    if instance.accepted:
        mail = instance.commentator.email
        send_mail(
            "Ваш отклик принят",
            "Ваш отклик на объявление принят автором",
            settings.DEFAULT_FROM_EMAIL,
            [mail],
            fail_silently=False,
            )
    # автору, пришел коммент
    else:
        mail = instance.post.author.author.email

        send_mail(
            "Новый отклик",
            "На ваше объявление пришел новый отклик!",
            settings.DEFAULT_FROM_EMAIL,
            [mail],
            fail_silently=False,
            )


@receiver(go_mail, sender='Weekly')
def weekly_mailing_list(sender, **kwargs):
    post_set = Post.objects.filter(creation_date__gt=(datetime.date.today() - datetime.timedelta(days=7)))
    if post_set:
        post_list = str(post_set)
        print(post_list)
        for user in User.objects.all():
            msg = EmailMultiAlternatives(
                subject='Новые объявления за неделю',
                body=post_list,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            html_content = render_to_string(
                'weekly_news.html',
                {
                    'posts': post_set,
                    'recipient': user.username
                }
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    else:
        for user in User.objects.all():
            send_mail(
                "Новости портала",
                "Новых объявлений за неделю не было",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
                )
