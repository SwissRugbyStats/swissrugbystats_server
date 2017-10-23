# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from swissrugbystats.crawler.SRSCrawler import SRSCrawler
from swissrugbystats.crawler.ConcurrentSRSCrawler import SRSAsyncCrawler
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.core.models import Team

def update_statistics(log_to_db=True):
    """

    :param log_to_db:
    :return:
    """
    teams = Team.objects.all()

    if log_to_db:
        CrawlerLogMessage.objects.create(
            message="Statistics update started."
        )

    # get current timestamp to calculate time needed for script exec
    start_time = datetime.datetime.now()

    for t in teams:
        try:
            print(u"update {}".format(t.name))
            t.update_statistics()
        except Exception as e:
            print(u"Exception! {}".format(e))

    if log_to_db:
        CrawlerLogMessage.objects.create(
            message=u"Statistics update complete.\n{0} team statistics updated\nTime needed: {1}".format(teams.count(),(datetime.datetime.now() - start_time))
        )

def crawl_and_update(deep_crawl=True, season=settings.CURRENT_SEASON, async=False, log_to_db=True):
    if (async):
        crawler = SRSAsyncCrawler(enable_logging=log_to_db)
    else:
        crawler = SRSCrawler(enable_logging=log_to_db)
    crawler.start(season, deep_crawl)

    crawler.log("Statistics update started.")

    # get current timestamp to calculate time needed for script exec
    start_time = datetime.datetime.now()

    teams = Team.objects.all()
    for t in teams:
        try:
            print(u"update {}".format(t.name))
            t.update_statistics()
        except Exception as e:
            print(u"Exception! {}".format(e))

    crawler.log(u"Statistics update complete.\n{0} team statistics updated\nTime needed: {1}".format(teams.count(),(datetime.datetime.now() - start_time)))