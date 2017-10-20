# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from swissrugbystats.crawler import tasks


class Command(BaseCommand):

    """
    Custom manage.py command to crawl the source website for all the games of the current season.

    https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
    """

    help = 'Crawl the source website for all the games of the current season.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('season_ids', nargs='*', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--deep',
            action='store_true',
            dest='deep',
            default=False,
            help='Crawl deep, which means to follow pagination.'
        )

    def handle(self, *args, **options):
        # create dict to hold the function arguments
        args = {'deep_crawl': False}
        if options.get('deep'):
            args['deep_crawl'] = True
        if options.get('season_ids'):
            for season in options.get('season_ids'):
                tasks.update_all(season=season, **args)
        else:
            tasks.update_all(**args)