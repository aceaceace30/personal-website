import requests
from django.conf import settings
from django.core.mail import send_mail

from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from django.urls import reverse

from portfolio.models import Project


class Command(BaseCommand):
    help = 'Check for broken urls across the pages available for website'

    broken_links = []
    html_message = '<ul>'

    def handle(self, *args, **options):
        for url in self.get_website_urls():
            print(f'Scrapping data for url: {url}')
            page = requests.get(url)
            self.get_broken_links(page.content)

        self.html_message += '</ul>'

        print(f'Broken links found: {self.broken_links}')
        if self.broken_links:
            send_mail(
                'List of broken links on the website.',
                '',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_ADMIN],
                html_message=self.html_message,
                fail_silently=False
            )

    @staticmethod
    def get_website_urls():
        project_urls = [settings.DOMAIN_NAME + reverse('homepage')]

        # get all project details
        for slug in Project.objects.values_list('slug', flat=True):
            project_url_base = reverse('portfolio:project_details', kwargs={'slug': slug})
            project_urls.append(settings.DOMAIN_NAME + project_url_base)

        return project_urls

    def get_broken_links(self, content):
        soup = BeautifulSoup(content, 'html.parser')

        for elem in soup.find_all('a'):
            href_value = elem.get('href')
            if href_value.startswith(('https://', 'http://')):
                response = requests.get(href_value)
                if response.status_code != 200:
                    self.broken_links.append((href_value, response.status_code))
                    self.html_message += f'<li>{href_value} - {response.status_code}</li>'

