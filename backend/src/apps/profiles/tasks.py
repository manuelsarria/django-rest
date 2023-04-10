# celeryApp/__init__.py
from django.core.mail import send_mail
# app = Celery('tasks', broker='redis://localhost:6379/0')
from src.celery import app

@app.task
def send_periodic_email():
    send_mail(
        'Asunto del correo: asunto',
        'Cuerpo del correo: cuerpo',
        'manuell.sarria@gmail.com',
        ['manuellemaure.s@gmail.com'],
        fail_silently=False,
    )