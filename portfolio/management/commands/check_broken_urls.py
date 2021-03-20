from django.core.management import BaseCommand
from portfolio.scraper import LinkChecker


class Command(BaseCommand):
    help = 'Check for broken urls across the pages available for website'

    def handle(self, *args, **options):
        link_checker = LinkChecker()
        link_checker.run()
