import requests
import logging
from datetime import datetime
from django.utils import timezone
from BeautifulSoup import BeautifulSoup
from swissrugby.models import Team, League, Game, GameParticipation, Venue, Referee

# create logger
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s- %(message)s', datefmt='%d.%m.%Y %I:%M:%S ')

# TODO: option to choose if wanting to make a deep crawl (all games), or just a shallow one (only first page of every league)
# TODO: try to combine crawlLeagueFixtures and crawlLeagueResults into one function
# TODO: add verbose option, don't show all the print() messages per default
# TODO: log count of objects at beginning, count of objects created / updated and count of objects after script completion
# TODO: save forfaits
# TODO: print summary of fetched data and how long it took at the end
# TODO: detect playoff and playdown games
# TODO: possibility to get old seasons (like 2013/2014)


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

leagueTeams = [(l, "http://www.suisserugby.com/competitions/" + l + ".html") for l in leagues]
leagueFixtures = [(l, "http://www.suisserugby.com/competitions/" + l + "/lt/fixtures.html") for l in leagues]
leagueResults = [(l, "http://www.suisserugby.com/competitions/" + l + "/lt/results.html") for l in leagues]


def crawlLeagueTeams(leagueUrl):

    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    for url in leagueUrl:
        r = requests.get(url[1], headers=headers)
        soup = BeautifulSoup(r.text)
        table = soup.find('table', attrs={'class': 'table'})

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) > 0:
                # parse Teamname and remove leading and tailing spaces
                team = cells[1].find(text=True).strip()
                if not Team.objects.filter(name=team):
                    t = Team(name=team)
                    t.save()
                    print "Team " + str(t) + " created"

# leagueResultsUrl is an array of [leagueShortCode, leagueUrl] tuples
def crawlLeagueResults(leagueResultsUrl):
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    # url is tupel of [leagueName, leagueUrl]
    for url in leagueResultsUrl:
        r = requests.get(url[1], headers=headers)
        soup = BeautifulSoup(r.text)
        table = soup.find('table', attrs={'class': 'table'})
        league = League.objects.filter(shortCode=url[0])[0]

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) > 0:

                # get host and guest team
                teams = cells[2].find(text=True)        # teams
                teams2 = teams.split(' - ')

                host = Team.objects.filter(name=teams2[0].strip())
                if not host:
                    logging.error("Hostteam not found: "+teams2[0].strip())
                    logging.error(row)
                    print "Hostteam not found: "+teams2[0].strip()
                    continue
                else:
                    host = host[0]
                guest = Team.objects.filter(name=teams2[1].strip())
                if not guest:
                    logging.error("Guestteam not found: "+teams2[1].strip())
                    logging.error(row)
                    print "Guestteam not found: "+teams2[1].strip()
                    continue
                else:
                    guest = guest[0]

                # check if game is already stored, if so, update the existing one
                fsrUrl = cells[0].find('a')['href']
                if not Game.objects.filter(fsrUrl=fsrUrl):
                    game = Game()
                    hostParticipant = GameParticipation(team=host)
                    guestParticipant = GameParticipation(team=guest)
                else:
                    game = Game.objects.filter(fsrUrl=fsrUrl)[0]
                    hostParticipant = game.host
                    guestParticipant = game.guest


                # parse date and set timezone
                date = cells[1].find(text=True)
                d1 = timezone.get_current_timezone().localize(datetime.strptime(date, '%d.%m.%Y %H:%M'))
                d2 = d1.strftime('%Y-%m-%d %H:%M%z')
                game.date = d2

                game.league = league
                game.fsrID = cells[0].find(text=True)
                game.fsrUrl = cells[0].find('a')['href']

                # Game details & team logos

                # make new request to game detail page
                r2 = requests.get(game.fsrUrl, headers=headers)
                soup2 = BeautifulSoup(r2.text)
                table2 = soup2.find('table')
                rows = table2.findAll('tr')

                host.logo = rows[1].findAll('td')[0].find('img')['src']   # logo host
                guest.logo = rows[1].findAll('td')[2].find('img')['src']  # logo guest

                venueName = rows[3].findAll('td')[1].find(text=True)     # venue
                if not Venue.objects.filter(name=venueName):
                    venue = Venue()
                    venue.name = venueName
                    print("Venue " + venueName + " created")
                else:
                    venue = Venue.objects.filter(name=venueName)[0]


                scoreRow = 4
                if rows[4].findAll('td')[1].find(text=True).strip() == "Forfait":
                    scoreRow += 1
                    #TODO: save forfait in db

                hostParticipant.score = int(rows[scoreRow].findAll('td')[0].find(text=True))          # score host
                guestParticipant.score = int(rows[scoreRow].findAll('td')[2].find(text=True))         # score guest
                hostParticipant.tries = int(rows[scoreRow+1].findAll('td')[0].find(text=True))          # tries host
                guestParticipant.tries = int(rows[scoreRow+1].findAll('td')[2].find(text=True))         # tries guest
                hostParticipant.redCards = int(rows[scoreRow+2].findAll('td')[0].find(text=True))       # red cards host
                guestParticipant.redCards = int(rows[scoreRow+2].findAll('td')[2].find(text=True))      # red cards guest

                # referee is not always there
                if len(rows)>=scoreRow+5:
                    refName = rows[scoreRow+4].findAll('td')[1].find(text=True).strip()     # referee
                    # TODO: save performance by not doing reassigning referee if aready set
                    if not Referee.objects.filter(name=refName):
                        referee = Referee()
                        referee.name = refName
                        print("Referee " + refName + " created")
                    else:
                        referee = Referee.objects.filter(name=refName)[0]
                    referee.save()
                    game.referee = referee

                host.save()
                guest.save()
                hostParticipant.team = host
                hostParticipant.save()
                guestParticipant.team = guest
                guestParticipant.save()
                game.host = hostParticipant
                game.guest = guestParticipant

                venue.save()
                game.venue = venue

                game.save()

                print "GameResult " + str(Game.objects.get(id=game.id)) + " created / updated"

            # recursively parse all next sites if there are any
            pagination = soup.find('div', attrs={'class': 'pagination'})
            current = int(pagination.find('span', attrs={'class': 'current'}).find(text=True))
            if current == 1:
                for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                    if int(page.find(text=True)) > current:
                        nextUrl = [(league.shortCode, page['href'])]
                        crawlLeagueResults(nextUrl)


def crawlLeagueFixtures(leagueFixturesUrl):
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    for url in leagueFixturesUrl:
        r = requests.get(url[1], headers=headers)
        soup = BeautifulSoup(r.text)
        table = soup.find('table', attrs={'class': 'table'})
        league = League.objects.filter(shortCode=url[0])[0]

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) > 0:

                # get host and guest team
                teams = cells[2].find(text=True)        # teams
                teams2 = teams.split(' - ')

                host = Team.objects.filter(name=teams2[0].strip())
                if not host:
                    logging.error("Hostteam not found: "+teams2[0].strip())
                    logging.error(row)
                    print "Hostteam not found: "+teams2[0].strip()
                    continue
                else:
                    host = host[0]
                guest = Team.objects.filter(name=teams2[1].strip())
                if not guest:
                    logging.error("Guestteam not found: "+teams2[1].strip())
                    logging.error(row)
                    print "Guestteam not found: "+teams2[1].strip()
                    continue
                else:
                    guest = guest[0]

                # check if game is already stored, if so, update the existing one
                fsrUrl = cells[0].find('a')['href']
                if not Game.objects.filter(fsrUrl=fsrUrl):
                    game = Game()
                    hostParticipant = GameParticipation(team=host)
                    guestParticipant = GameParticipation(team=guest)
                else:
                    game = Game.objects.filter(fsrUrl=fsrUrl)[0]
                    hostParticipant = game.host
                    guestParticipant = game.guest


                # parse date and set timezone
                date = cells[1].find(text=True)
                d1 = timezone.get_current_timezone().localize(datetime.strptime(date, '%d.%m.%Y %H:%M'))
                d2 = d1.strftime('%Y-%m-%d %H:%M%z')
                game.date = d2

                game.league = league
                game.fsrID = cells[0].find(text=True)
                game.fsrUrl = cells[0].find('a')['href']

                # Game details & team logos

                # make new request to game detail page
                r2 = requests.get(game.fsrUrl, headers=headers)
                soup2 = BeautifulSoup(r2.text)
                table2 = soup2.find('table')
                rows = table2.findAll('tr')

                host.logo = rows[1].findAll('td')[0].find('img')['src']   # logo host
                guest.logo = rows[1].findAll('td')[2].find('img')['src']  # logo guest
                venueName = rows[3].findAll('td')[1].find(text=True)     # venue
                if not Venue.objects.filter(name=venueName):
                    venue = Venue()
                    venue.name = venueName
                    print("Venue " + venueName + " created")
                else:
                    venue = Venue.objects.filter(name=venueName)[0]

                host.save()
                guest.save()
                hostParticipant.team = host
                hostParticipant.save()
                guestParticipant.team = guest
                guestParticipant.save()
                game.host = hostParticipant
                game.guest = guestParticipant

                venue.save()
                game.venue = venue

                game.save()

                print "GameFixture " + str(Game.objects.get(id=game.id)) + " created / updated"

            # recursively parse all next sites if there are any
            pagination = soup.find('div', attrs={'class': 'pagination'})
            current = int(pagination.find('span', attrs={'class': 'current'}).find(text=True))
            if current == 1:
                for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                    if int(page.find(text=True)) > current:
                        nextUrl = [(league.shortCode, page['href'])]
                        crawlLeagueFixtures(nextUrl)

'''
print "Teams:\n"

#print str(crawlLeagueTeams(leagues))


print "\n------------------\n"

print "League Scores:\n"

#print str(crawlLeagueResults(leagues))

print "\n------------------\n"

print "League Fixtures:\n"

#print str(crawlLeagueFixtures(leagueFixtures))
'''