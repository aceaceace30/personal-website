from django.conf import settings
from django.core.mail import send_mail

from personal_profile.celery import app


@app.task(name='send_mail_task', ignore_result=True)
def send_mail_task(subject, email, message):
    """Task for sending email"""
    send_mail(
        f'{subject} - {email}',
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_ADMIN],
        fail_silently=False
    )
