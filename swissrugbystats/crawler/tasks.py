import datetime
from django_admin_conf_vars.global_vars import config
import logging
from swissrugbystats.crawler.crawler import SRSCrawler
from swissrugbystats.core.models import Competition, Season

# create logger
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s- %(message)s', datefmt='%d.%m.%Y %I:%M:%S ')


def update_all(deep_crawl=True, season=config.CURRENT_SEASON):
    """
    crawl suisserugby.com for the latest data
    :param deep_crawl: crawl through pagination
    :return: none
    """
    current_season = Season.objects.get(id=season)
    logging.info("update started for season {}".format(current_season))

    # get current timestamp to calculate time needed for script exec
    start_time = datetime.datetime.now()

    print "------------------------------------------------------------------"
    print ""

    print "Getting latest data from suisserugby.com"
    if deep_crawl:
        print "    deep_crawl = True - following pagination"
    else:
        print "    deep_crawl = False (default) - not following pagination"

    print ""
    print "------------------------------------------------------------------"
    print ""

    crawler = SRSCrawler()

    # update team table
    print("crawl Teams")
    #crawler.crawl_teams_async([(c.league.shortCode, c.get_league_url(), c.id) for c in Competition.objects.filter(season=s)])
    teams_count = crawler.crawl_teams([(c.league.shortCode, c.get_league_url(), c.id) for c in Competition.objects.filter(season=current_season)])

    # update game table with fixtures
    print("current season:" + config.CURRENT_SEASON)
    #crawler.crawl_fixtures_async([(c.league.shortCode, c.get_fixtures_url(), c.id) for c in Competition.objects.filter(season=s)], deep_crawl)
    fixtures_count = crawler.crawl_fixtures([(c.league.shortCode, c.get_fixtures_url(), c.id) for c in Competition.objects.filter(season=current_season)], deep_crawl)

    # update game table with results
    #crawler.crawl_results_async([(c.league.shortCode, c.get_results_url(), c.id) for c in Competition.objects.filter(season=s)], deep_crawl)
    result_count = crawler.crawl_results([(c.league.shortCode, c.get_results_url(), c.id) for c in Competition.objects.filter(season=current_season)], deep_crawl)

    #fixtures_count = crawler.get_fixtures_count()
    #result_count = crawler.get_results_count()

    print ""
    print "------------------------------------------------------------------"
    print ""
    print "{} {}".format(teams_count, "teams crawled")
    print "{} {}".format(result_count, "results crawled")
    print "{} {}".format(fixtures_count, "fixtures crawled")

    print ""
    print "{} {}".format("Time needed:", (datetime.datetime.now() - start_time))
    print ""

