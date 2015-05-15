import datetime
import django
import os
import sys
import logging
import pytz

from django.utils import timezone

# import models from swissrugbystats, all django models must be imported BENEATH this block
sys.path.append("/home/chregi/Documents/git/swissrugbystats")
os.environ["DJANGO_SETTINGS_MODULE"] = "swissrugbystats.settings"
timezone.activate(pytz.timezone("Europe/Zurich"))
django.setup()

from crawler import SRSCrawler

# create logger
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s- %(message)s', datefmt='%d.%m.%Y %I:%M:%S ')

from swissrugby.models import League

leagues = [
    "u16-east",
    "u16-west",
    "u18",
    "league-1-east",
    "league-1-west",
    "lnc-east",
    "lnc-west",
    "lnb",
    "lna"
]


def update_all(deep_crawl=False):
    '''
    crawl suisserugby.com for the latest data
    :param deep_crawl: crawl through pagination
    :return: none
    '''

    logging.info("update started")

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

    initLeagueDB()
    c = SRSCrawler()

    # update team table
    c.crawl_teams_per_league([(l.shortCode, l.getLeagueUrl()) for l in League.objects.all()])

    # update game table with fixtures
    fixtures_count = c.crawl_fixtures_async([(l.shortCode, l.getFixturesUrl()) for l in League.objects.all()], deep_crawl)

    # update game table with results
    result_count = c.crawl_results_async([(l.shortCode, l.getResultsUrl()) for l in League.objects.all()], deep_crawl)

    print ""
    print "------------------------------------------------------------------"
    print ""
    print "{} {}".format(result_count, "results crawled")
    print "{} {}".format(fixtures_count, "fixtures crawled")

    print ""
    print "{} {}".format("Time needed:", (datetime.datetime.now() - start_time))
    print ""

def initLeagueDB():
    # initialize if still empty
    if League.objects.count() == 0:
        print "Initialize leagues"
        for league in leagues:
            print league + " created"
            l = League(name=league, shortCode=league)
            l.save()
    else:
        print "Leagues already initialized"


update_all()