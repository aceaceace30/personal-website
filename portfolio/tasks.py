from django.conf import settings
from django.core.mail import send_mail

from personal_website.celery import app
from portfolio.scraper import LinkChecker


@app.task(name='send_mail_task', ignore_result=True)
def send_mail_task(subject: str, email: str, message: str) -> None:
    """Task for sending email"""
    send_mail(
        f'{subject} - {email}',
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_ADMIN],
        fail_silently=False
    )


@app.task(name='check_site_broken_links', ignore_result=True)
def check_site_broken_links() -> None:
    """Task for checking site broken links and sending email notification if there is one"""
    link_checker = LinkChecker()
    link_checker.run()
