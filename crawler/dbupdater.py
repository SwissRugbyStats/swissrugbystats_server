import os, sys

sys.path.append("/home/chregi/Documents/git/swissrugbystats")
os.environ["DJANGO_SETTINGS_MODULE"] = "swissrugbystats.settings"

from crawler import crawlLeagueResults
from crawler import crawlLeagueTeams
from crawler import crawlLeagueFixtures

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
    print "updateAll"

def initLeagueDB():
    # initialize if still empty
    if League.objects.count() == 0:
        print "Initialize leagues"
        for league in leagues:
            print league + created
            l = League(name=league, shortCode=league)
            l.save()
    else:
        print "Leagues already initialized"


def createTeamDB():
    print "create TeamDB"

#initLeagueDB()
