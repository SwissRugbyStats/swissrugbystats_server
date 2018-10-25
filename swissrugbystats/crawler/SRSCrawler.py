# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse

from swissrugbystats.core.models import Competition, Season
from swissrugbystats.crawler.crawler import TeamCrawler, ResultCrawler, \
    FixtureCrawler
from swissrugbystats.crawler.models import CrawlerLogMessage


# TODO: try to combine crawlLeagueFixtures and crawlLeagueResults into one function
# TODO: add verbose option, don't show all the print() messages per default
# TODO: log count of objects at beginning, count of objects created / updated and count of objects after script completion
# TODO: save forfaits --> Done
# TODO: print summary of fetched data and how long it took at the end --> partially done
# TODO: detect playoff and playdown games
# TODO: possibility to get old seasons (like 2013/2014)
# TODO: concurrency


class SRSCrawler(object):
    """
    Todo: document.
    """

    def __init__(self, headers={'User-Agent': 'Mozilla 5.0'},
        enable_logging=True):
        """
        Create SRSCrawler instance.
        :param headers: HTTP Headers to send with.
        :return: void
        """
        self.headers = headers
        self.statistics = {
            'teams': 0,
            'fixtures': 0,
            'results': 0
        }
        self.log_to_db = enable_logging

    @classmethod
    def get_classname(cls):
        return cls.__name__

    def log(self, msg):
        """
        helper method that should be put into separate class.
        actually logging should be completely moved into the crawler
        :param msg:
        :param log_to_db:
        :return:
        """
        if self.log_to_db:

            msg = u'{}: {}'.format(self.get_classname(), msg)
            logmsg = CrawlerLogMessage.objects.create(message=msg)

            if settings.SLACK_WEBHOOK_URL:
                # post update to slack
                try:
                    import requests
                    import json

                    r = 'admin:{}_{}_change'.format(logmsg._meta.app_label,
                                                    logmsg._meta.model_name)

                    text = logmsg.message + "\n<{}{}|Click here>".format(
                        settings.BASE_URL,
                        reverse(r, args=(logmsg.id,))
                    )
                    url = settings.SLACK_WEBHOOK_URL
                    payload = {"text": text}
                    headers = {'content-type': 'application/json'}

                    response = requests.post(url, data=json.dumps(payload),
                                             headers=headers)

                except Exception as e:
                    print(e)

    def start(self,
        season=settings.CURRENT_SEASON,
        deep_crawl=False,
        competition_filter=[]
    ):
        # TODO: what to do if no season present?
        current_season = Season.objects.get(id=season)

        self.log(
            u"Update started for season {}.\n    deep crawl = {}\n     competition_filter = {}".format(
                current_season, deep_crawl, competition_filter))

        # get current timestamp to calculate time needed for script exec
        start_time = datetime.now()

        print(
            "------------------------------------------------------------------")
        print("")

        print(u"{}: Getting data from suisserugby.com for season {}".format(
            self.get_classname(), Season.objects.filter(id=season).first()))
        if deep_crawl:
            print("    deep_crawl = True - following pagination")
        else:
            print("    deep_crawl = False (default) - not following pagination")

        print("    competition_filter = {}".format(competition_filter))

        print("")
        print(
            "------------------------------------------------------------------")
        print("")

        # competitions to crawl
        competitions = Competition.objects.all()
        if current_season:
            competitions = Competition.objects.filter(season=current_season)
        if competition_filter:
            competitions = Competition.objects.filter(pk__in=competition_filter)

        # update team table
        print("crawl Teams")
        TeamCrawler.crawl(
            [(c.league.shortcode, c.get_league_url(), c.id) for c in
             competitions])

        # update game table with fixtures
        print(u"current season:".format(settings.CURRENT_SEASON))
        FixtureCrawler.crawl(
            [(c.league.shortcode, c.get_fixtures_url(), c.id) for c in
             competitions], deep_crawl)

        # update game table with results
        ResultCrawler.crawl(
            [(c.league.shortcode, c.get_results_url(), c.id) for c in
             competitions], deep_crawl)

        results_log = u"""
                Crawling completed.\n
                {0} teams crawled\n
                {1} results crawled\n
                {2} fixtures crawled\n
                Time needed: {3}
            """.format(self.statistics.get('teams', 0),
                       self.statistics.get('results', 0),
                       self.statistics.get('fixtures', 0),
                       (datetime.now() - start_time))

        self.log(results_log)

        print("")
        print(
            "------------------------------------------------------------------")
        print("")
        print(results_log)
        print("")
