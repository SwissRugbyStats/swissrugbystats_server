import os
import sys
import django
import logging
import pytz
from datetime import datetime
from django.utils import timezone

# import models from swissrugbystats
sys.path.append("/home/chregi/Documents/git/swissrugbystats")
os.environ["DJANGO_SETTINGS_MODULE"] = "swissrugbystats.settings"
timezone.activate(pytz.timezone("Europe/Zurich"))
django.setup()


# create logger
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s- %(message)s', datefmt='%d.%m.%Y %I:%M:%S ')

import crawler

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

def updateAll():

    logging.info("update started")

    initLeagueDB()

    # update team table
    crawler.crawlLeagueTeams([(l.shortCode, l.getLeagueUrl()) for l in League.objects.all()])

    # update game table with results
    crawler.crawlLeagueResults([(l.shortCode, l.getResultsUrl()) for l in League.objects.all()])

    # update game table with fixtures
    crawler.crawlLeagueFixtures([(l.shortCode, l.getFixturesUrl()) for l in League.objects.all()])

    print "updateAll"


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


updateAll()