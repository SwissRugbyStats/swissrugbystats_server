# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

from swissrugbystats.core.SeasonManager import SeasonManager
from swissrugbystats.core.models import Competition, Season
from swissrugbystats.crawler.crawler.CompetitionCrawler import CompetitionCrawler
from swissrugbystats.crawler.crawler.FixtureCrawler import FixtureCrawler
from swissrugbystats.crawler.crawler.ResultCrawler import ResultCrawler
from swissrugbystats.crawler.crawler.TeamCrawler import TeamCrawler
from swissrugbystats.crawler.log.CrawlerLogMixin import CrawlerLogMixin


# TODO: try to combine crawlLeagueFixtures and crawlLeagueResults into one function
# TODO: add verbose option, don't show all the print() messages per default
# TODO: log count of objects at beginning, count of objects created / updated and count of objects after script completion
# TODO: save forfaits --> Done
# TODO: print summary of fetched data and how long it took at the end --> partially done
# TODO: detect playoff and playdown games
# TODO: possibility to get old seasons (like 2013/2014)
# TODO: concurrency


class SRSCrawler(CrawlerLogMixin):
    """
    Todo: document.
    """

    def __init__(self, headers={'User-Agent': 'Mozilla 5.0'}, enable_logging: bool = True):
        """
        Create SRSCrawler instance.
        :param headers: HTTP Headers to send with.
        :return: void
        """
        super().__init__()
        self.headers = headers
        self.statistics = {
            'teams': 0,
            'fixtures': 0,
            'results': 0
        }
        self.log_to_db = enable_logging

    @classmethod
    def get_classname(cls) -> str:
        return cls.__name__

    def start(self,
              season_id: int = None,
              deep_crawl: bool = False,
              competition_filter: List[int] = []
              ):
        if season_id:
            season = Season.objects.get(id=season)

        if not season_id or not season:
            season = SeasonManager.get_current_season()

        # get current timestamp to calculate time needed for script exec
        start_time = datetime.now()

        start_msg: str = u"""
------------------------------------------------------------------
{}: Getting data from suisserugby.com for season {} {}
    deep_crawl = {} (default: True) - following pagination or not
    competition_filter = {}
------------------------------------------------------------------
        
        """.format(self.get_classname(), season, season, deep_crawl, competition_filter)

        self.log(start_msg, True, True)

        # first of, crawl competitions
        CompetitionCrawler.crawl()

        # competitions to crawl
        competitions = Competition.objects.all()
        if season:
            competitions = Competition.objects.filter(season=season)
        if competition_filter:
            competitions = Competition.objects.filter(pk__in=competition_filter)

        # update team table
        self.statistics['teams'] = TeamCrawler.crawl(competitions)

        # update game table with fixtures
        self.statistics['fixtures'] = FixtureCrawler.crawl(competitions)

        # update game table with results
        self.statistics['results'] = ResultCrawler.crawl(competitions)

        end_msg: str = u"""

------------------------------------------------------------------
Crawling completed.\n
    {0} teams crawled
    {1} results crawled
    {2} fixtures crawled\n
    Time needed: {3}
------------------------------------------------------------------
        
        """.format(self.statistics.get('teams', 0),
                   self.statistics.get('results', 0),
                   self.statistics.get('fixtures', 0),
                   (datetime.now() - start_time))

        self.log(end_msg, True, True)
