import os
import sys
import django
import logging
import pytz
from datetime import datetime
from django.utils import timezone

sys.path.append("/home/chregi/Documents/git/swissrugbystats")
os.environ["DJANGO_SETTINGS_MODULE"] = "swissrugbystats.settings"
timezone.activate(pytz.timezone("Europe/Zurich"))
django.setup()


# create logger
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s- %(message)s', datefmt='%d.%m.%Y %I:%M:%S ')

import crawler

from swissrugby.models import Team
from swissrugby.models import League
from swissrugby.models import Game

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

    # update team table
    teams = crawler.crawlLeagueTeams([(l.shortCode, l.getLeagueUrl()) for l in League.objects.all()])
    for league in teams:
        for team in league[1]:
            if not Team.objects.filter(name=team):
                t = Team(name=team)
                t.save()
                print "Team " + str(t) + " created"


    # update game table with fixtures
    gameFixtures = crawler.crawlLeagueFixtures([(l.shortCode, l.getFixturesUrl()) for l in League.objects.all()])
    for league in gameFixtures:
        for game in league[1]:
            l = League.objects.filter(shortCode=league[0])[0]
            # parse date and set timezone
            d1 = timezone.get_current_timezone().localize(datetime.strptime(game[2], '%d.%m.%Y %H:%M'))
            d2 = d1.strftime('%Y-%m-%d %H:%M%z')

            host = Team.objects.filter(name=game[3])
            if not host:
                logging.error("Hostteam not found: "+game[3])
                print "Hostteam not found: "+game[3]

            guest = Team.objects.filter(name=game[4])
            if not guest:
                logging.error("Guestteam not found: "+game[3])
                print "Guestteam not found: "+game[4]

            logging.info("Fixture: " + str(game))

            if not Game.objects.filter(fsrUrl=game[1]):
                g = Game(league=l, fsrID=game[0], fsrUrl=game[1], date=d2, hostTeam=host[0], guestTeam=guest[0])
                g.save()
            else:
                g = Game.objects.filter(fsrUrl=game[1])[0]
                g.league = l
                g.date = d2
                g.save()

    # update game table with results
    gameResults = crawler.crawlLeagueResults([(l.shortCode, l.getResultsUrl()) for l in League.objects.all()])
    for league in gameResults:
        for game in league[1]:
            l = League.objects.filter(shortCode=league[0])[0]
            # parse date and set timezone
            d1 = timezone.get_current_timezone().localize(datetime.strptime(game[2], '%d.%m.%Y %H:%M'))
            d2 = d1.strftime('%Y-%m-%d %H:%M%z')

            logging.info("Result: " + str(game))

            if not Game.objects.filter(fsrUrl=game[1]):
                g = Game(league=l, fsrID=game[0], fsrUrl=game[1], date=d2, hostTeam=Team.objects.filter(name=game[3])[0], guestTeam=Team.objects.filter(name=game[4])[0], hostScore=game[5], guestScore=game[6])
                g.save()
            else:
                g = Game.objects.filter(fsrUrl=game[1])[0]
                g.league = l
                g.date = d2
                g.hostScore = game[5]
                g.guestScore = game[6]
                g.save()


    print "updateAll"

def initLeagueDB():
    # initialize if still empty
    if League.objects.count() == 0:
        print "Initialize leagues"
        for league in leagues:
            print league + "created"
            l = League(name=league, shortCode=league)
            l.save()
    else:
        print "Leagues already initialized"


def updateTeamDB():
    print "create TeamDB"

updateAll()
