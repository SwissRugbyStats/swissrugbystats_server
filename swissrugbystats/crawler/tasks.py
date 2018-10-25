# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from swissrugbystats.core.models import Team
from swissrugbystats.crawler.ConcurrentSRSCrawler import SRSAsyncCrawler
from swissrugbystats.crawler.SRSCrawler import SRSCrawler


def update_statistics(log_to_db=True):
    """

    :param log_to_db:
    :return:
    """
    crawler = SRSCrawler(enable_logging=log_to_db)
    teams = Team.objects.all()

    crawler.log("Statistics update started.")

    # get current timestamp to calculate time needed for script exec
    start_time = datetime.datetime.now()

    for t in teams:
        try:
            print(u"Update statistics for: {}".format(t.name))
            t.update_statistics()
        except Exception as e:
            print(u"Exception! {}".format(e))

    statistic_success_message = u"Statistics update complete.\n{0} team statistics updated\nTime needed: {1}".format(teams.count(),(datetime.datetime.now() - start_time))

    print(statistic_success_message)
    crawler.log(statistic_success_message)


def crawl_and_update(deep_crawl=True, season=settings.CURRENT_SEASON, async=False, log_to_db=True):
    """

    :param deep_crawl:
    :param season:
    :param async:
    :param log_to_db:
    :return:
    """
    if (async):
        crawler = SRSAsyncCrawler(enable_logging=log_to_db)
    else:
        crawler = SRSCrawler(enable_logging=log_to_db)

    crawler.start(season, deep_crawl)

    update_statistics(log_to_db)
