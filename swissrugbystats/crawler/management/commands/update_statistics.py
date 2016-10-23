# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from swissrugbystats.crawler import tasks


class Command(BaseCommand):

    """
    Custom manage.py command to update the team statistics.

    https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
    """

    help = 'Update the team statistics.'

    def handle(self, *args, **options):
        tasks.update_statistics()