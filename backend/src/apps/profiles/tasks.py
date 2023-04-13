# # celeryApp/__init__.py
# from django.core.mail import send_mail
# # app = Celery('tasks', broker='redis://localhost:6379/0')
# from src.celery import app

# @app.task
# def send_periodic_email():
#     send_mail(
#         'Asunto del correo: asunto',
#         'Cuerpo del correo: cuerpo',
#         'manuell.sarria@gmail.com',
#         ['manuellemaure.s@gmail.com'],
#         fail_silently=False,
#     )

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import json

print( 'execute the task periodic')

@shared_task
def send_periodic_email():
    send_mail(
        'Subject',
        'Body',
        'manuellemaure.s@gmail.com',
        ['manuell.sarria@gmail.com'],
        fail_silently=False,
    )
    
class send_periodic_email_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, send_periodic_email):
            return {
                "subject": obj.subject,
                "body": obj.body,
                "recipients": obj.recipients
            }
        return super().default(obj)