import os
from celery import Celery

from django.core.mail import send_mail
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.base')

app = Celery('src')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # ...
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        send_my_email.s('subject', 'message', 'from@example.com', ['to@example.com']),
    )

@app.task
def send_my_email(subject, message, fromEmail, recipients):
    send_mail(
        subject,
        message,
        fromEmail,
        recipients,
        fail_silently=False,
    )