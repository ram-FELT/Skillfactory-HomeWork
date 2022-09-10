import logging
from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.dispatch import Signal

logger = logging.getLogger(__name__)

go_mail = Signal()


def job1():
    go_mail.send_robust(sender='Weekly')


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def run():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        job1,
        trigger=CronTrigger(
            day_of_week="sun", hour="8", minute="00"
        ),
        id="job1",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added 'job1'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),

        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
        "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
