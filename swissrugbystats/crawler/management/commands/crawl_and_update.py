from django.core.management.base import BaseCommand, CommandError
from swissrugbystats.crawler import tasks


class Command(BaseCommand):

    """
    Custom manage.py command to crawl the source website.

    https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
    """

    help = 'Todo'

    # def add_arguments(self, parser):
    # Todo: make command more powerful, to import single users by username
    #     parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        tasks.update_all()