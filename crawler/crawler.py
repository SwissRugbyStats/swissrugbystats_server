from BeautifulSoup import BeautifulSoup
from datetime import datetime
from django.utils import timezone
from multiprocessing.pool import ThreadPool
from swissrugby.models import Team, League, Game, GameParticipation, Venue, Referee
import requests
import logging

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
# TODO: concurrency


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


class SRSCrawler(object):

    def __init__(self, processes=50):
        self.pool = ThreadPool(processes=processes)
        self.result_tasks = []
        self.fixture_tasks = []

    def crawl_teams(self, league_urls):
        '''
        :param leagueUrl: list of URLs to crawl for teams
        :return: -
        '''
        for url in league_urls:
            self.crawl_teams_per_league(url)

    def crawl_teams_async(self, league_urls):
        for url in league_urls:
            self.pool.apply_async(self.crawl_teams_per_league, (url))

    def crawl_teams_per_league(self, url):
        headers = {
            'User-Agent': 'Mozilla 5.0'
        }
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
                    print ("Team {0} created".format(str(t)))
                else:
                    print ("Team {0} already in DB".format(str(t)))

    def crawl_results(self, league_results_urls, deep_crawl=False):
        '''

        :param league_results_urls:    list of tuples [(league_shortcode, league_url), ..]
        :param deep_crawl:  defaults to False. Set True to follow pagination
        :return: number of crawled game results
        '''
        count = 0
        for url in league_results_urls:
            count += self.crawl_results_per_league(url, deep_crawl)

    def crawl_results_async(self, league_results_urls, deep_crawl=False):
        '''

        :param league_results_urls:    list of tuples [(league_shortcode, league_url), ..]
        :param deep_crawl:  defaults to False. Set True to follow pagination
        :return: -
        '''

        # url is tupel of (leagueName, leagueUrl)
        for url in league_results_urls:
            self.result_tasks += [self.pool.apply_async(self.crawl_results_per_league, ((url, deep_crawl)))]

    def get_results_count(self):
        '''
        wait for all pending tasks to finish and then summarize the results
        :return:
        '''
        count = 0
        for t in self.result_tasks:
            try:
                if type(t.get()) is int:
                    count += t.get()
            except Exception as e:
                print e
        self.result_tasks = []
        return count

    def crawl_results_per_league(self, url, deep_crawl):
        count = 0
        headers = {
            'User-Agent': 'Mozilla 5.0'
        }
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
                    # TODO: save performance by not reassigning referee if already set
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

                # increment game counter
                count += 1

            if deep_crawl:
                # recursively parse all next sites if there are any
                pagination = soup.find('div', attrs={'class': 'pagination'})
                current = int(pagination.find('span', attrs={'class': 'current'}).find(text=True))
                if current == 1:
                    for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                        if int(page.find(text=True)) > current:
                            nextUrl = [(league.shortCode, page['href'])]
                            count += self.crawl_results_async(nextUrl)
        return count

    def crawl_fixtures(self, league_fixtures_urls, deep_crawl=False):
        count = 0

        for url in league_fixtures_urls:
            count += self.crawl_fixture_per_league(url, deep_crawl)

        return count

    def crawl_fixtures_async(self, league_fixtures_urls, deep_crawl=False):
        '''
        Fetch all the fixtures asynchronously and add the AsynchronousResults to fixture_tasks
        :param league_fixtures_urls:
        :param deep_crawl:
        :return:
        '''
        for url in league_fixtures_urls:
            self.fixture_tasks += [self.pool.apply_async(self.crawl_fixture_per_league, ((url, deep_crawl)))]

    def get_fixtures_count(self):
        '''
        wait for all pending tasks to finish and then summarize the results
        :return:
        '''
        count = 0
        for t in self.fixture_tasks:
            try:
                if type(t.get()) is int:
                    count += t.get()
            except Exception as e:
                print e
        self.fixture_tasks = []
        return count

    def crawl_fixture_per_league(self, url, deep_crawl=False):
        count = 0
        headers = {
            'User-Agent': 'Mozilla 5.0'
        }
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

                # increment game counter
                count += 1

            if deep_crawl:
                # recursively parse all next sites if there are any
                pagination = soup.find('div', attrs={'class': 'pagination'})
                current = int(pagination.find('span', attrs={'class': 'current'}).find(text=True))
                if current == 1:
                    for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                        if int(page.find(text=True)) > current:
                            nextUrl = [(league.shortCode, page['href'])]
                            count += self.crawl_fixtures_async(nextUrl)
        return count