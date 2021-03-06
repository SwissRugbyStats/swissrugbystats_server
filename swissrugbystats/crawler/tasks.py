# -*- coding: utf-8 -*-
import datetime

from django.conf import settings

from swissrugbystats.core.models import Team, Game
from swissrugbystats.crawler.crawler.GameCrawler import GameCrawler
from swissrugbystats.crawler.crawler.SRSCrawler import SRSCrawler
from swissrugbystats.crawler.crawler.SRSCrawlerConcurrent import SRSCrawlerConcurrent


def update_statistics(log_to_db=True):
    """

    :param log_to_db:
    :return:
    """
    crawler = SRSCrawler()
    teams = Team.objects.all()

    start_msg = u"""

------------------------------------------------------------------
Statistics update started.
------------------------------------------------------------------
        
        """
    crawler.log(start_msg)

    # get current timestamp to calculate time needed for script exec
    start_time = datetime.datetime.now()

    for t in teams:
        try:
            print(u"Update statistics for: {}".format(t.name))
            t.update_statistics()
        except Exception as e:
            print(u"Exception! {}".format(e))

    end_msg = u"""

------------------------------------------------------------------
Statistics update complete.\n
    {0} team statistics updated\n
    Time needed: {1}
------------------------------------------------------------------
        
        """.format(teams.count(), (datetime.datetime.now() - start_time))

    crawler.log(end_msg)


def crawl_and_update(deep_crawl=True, season_id=None, async=False, competitions_filter=None,
                     log_to_db=True):
    """

    :param deep_crawl:
    :param season_id:
    :param async:
    :param competitions_filter:
    :param log_to_db:
    :return:
    """
    if async:
        crawler = SRSCrawlerConcurrent(enable_logging=log_to_db)
    else:
        crawler = SRSCrawler(enable_logging=log_to_db)

    crawler.start(season_id, deep_crawl, competitions_filter)

    update_statistics(log_to_db)


def crawl_game(game_id):
    """

    :param gameId:
    :return:
    """
    crawler = GameCrawler()
    crawler.start(game_id)
