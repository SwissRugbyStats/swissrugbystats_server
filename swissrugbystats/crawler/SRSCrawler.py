# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import smart_unicode
import logging
import requests
from swissrugbystats.core.models import Competition, Team, Season, Game, GameParticipation, Venue, Referee
from swissrugbystats.crawler.models import CrawlerLogMessage

# TODO: try to combine crawlLeagueFixtures and crawlLeagueResults into one function
# TODO: add verbose option, don't show all the print() messages per default
# TODO: log count of objects at beginning, count of objects created / updated and count of objects after script completion
# TODO: save forfaits --> Done
# TODO: print summary of fetched data and how long it took at the end --> partially done
# TODO: detect playoff and playdown games
# TODO: possibility to get old seasons (like 2013/2014)
# TODO: concurrency

class SRSCrawler(object):
    """
    Todo: document.
    """

    def __init__(self, headers={'User-Agent': 'Mozilla 5.0'}, enable_logging=True):
        """
        Create SRSCrawler instance.
        :param headers: HTTP Headers to send with.
        :return: void
        """
        self.headers = headers
        self.statistics = {
            'teams': 0,
            'fixtures': 0,
            'results': 0
        }
        self.log_to_db = enable_logging

    @classmethod
    def get_classname(cls):
        return cls.__name__

    def log(self, msg):
        """
        helper method that should be put into separate class.
        actually logging should be completely moved into the crawler
        :param msg:
        :param log_to_db:
        :return:
        """
        if self.log_to_db:

            msg = u'{}: {}'.format(self.get_classname(), msg)
            logmsg = CrawlerLogMessage.objects.create(message=msg)

            if settings.SLACK_WEBHOOK_URL:
                # post update to slack
                try:
                    import requests
                    import json

                    r = 'admin:{}_{}_change'.format(logmsg._meta.app_label, logmsg._meta.model_name)

                    text = logmsg.message + "\n<{}{}|Click here>".format(
                        settings.BASE_URL,
                        reverse(r, args=(logmsg.id,))
                    )
                    url = settings.SLACK_WEBHOOK_URL
                    payload = {"text": text}
                    headers = {'content-type': 'application/json'}

                    response = requests.post(url, data=json.dumps(payload), headers=headers)

                except Exception as e:
                    print(e)

    def start(self,
              season=settings.CURRENT_SEASON,
              deep_crawl=False,
              competition_filter=[]
              ):
        current_season = Season.objects.get(id=season)

        self.log(u"Update started for season {}.\n    deep crawl = {}\n     competition_filter = {}".format(current_season, deep_crawl, competition_filter))

        # get current timestamp to calculate time needed for script exec
        start_time = datetime.now()

        print("------------------------------------------------------------------")
        print("")

        print(u"{}: Getting data from suisserugby.com for season {}".format(self.get_classname(), Season.objects.filter(id=season).first()))
        if deep_crawl:
            print("    deep_crawl = True - following pagination")
        else:
            print("    deep_crawl = False (default) - not following pagination")

        print("    competition_filter = {}".format(competition_filter))

        print("")
        print("------------------------------------------------------------------")
        print("")

        # competitions to crawl
        competitions = Competition.objects.all()
        if current_season:
            competitions = Competition.objects.filter(season=current_season)
        if competition_filter:
            competitions = Competition.objects.filter(pk__in=competition_filter)

        # update team table
        print("crawl Teams")
        self.crawl_teams(
            [(c.league.shortcode, c.get_league_url(), c.id) for c in competitions])

        # update game table with fixtures
        print(u"current season:".format(settings.CURRENT_SEASON))
        self.crawl_fixtures([(c.league.shortcode, c.get_fixtures_url(), c.id) for c in competitions], deep_crawl)

        # update game table with results
        self.crawl_results([(c.league.shortcode, c.get_results_url(), c.id) for c in competitions], deep_crawl)

        results_log = u"""
                Crawling completed.\n
                {0} teams crawled\n
                {1} results crawled\n
                {2} fixtures crawled\n
                Time needed: {3}
            """.format(self.statistics.get('teams', 0), self.statistics.get('results', 0), self.statistics.get('fixtures', 0), (datetime.now() - start_time))

        self.log(results_log)

        print("")
        print("------------------------------------------------------------------")
        print("")
        print(results_log)
        print("")


    def crawl_teams(self, league_urls):
        """
        Go through all the urls in league_urls and call crawl_teams_per_league.
        :param self:
        :param league_urls: list of URLs to crawl for teams
        :return: number of fetched teams
        """
        for url in league_urls:
            self.crawl_teams_per_league(url)
        return self.statistics['teams']


    def crawl_teams_per_league(self, url, lock=None):
        """
        Fetch all the teams that are participating in a league.
        :param url: url of the league
        :return: number of fetched teams
        """
        count = 0
        print("crawl {}".format(url[1]))
        try:
            r = requests.get(url[1], headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            # find all tables of the rugbymanager plugin, to be sure to get all the information
            if soup:
                tables = soup.findAll('table', attrs={'class': 'table'})
            else:
                tables = []

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        cells = row.findAll('td')
                        if len(cells) > 0:
                            # check if we are looking at the season table and not a playdown / playoff / finals table
                            if len(cells) > 5:
                                team_name_raw = cells[1].find(text=True)
                                try:
                                    # parse Teamname and remove leading and tailing spaces
                                    team_name_unicode = smart_unicode(team_name_raw.strip())

                                    if not Team.objects.filter(name=team_name_unicode):
                                        t = Team(name=team_name_unicode)
                                        t.save()
                                        count += 1
                                        print(u"Team {0} created".format(t.__str__()))
                                    else:
                                        print(u"Team {0} already in DB".format(Team.objects.filter(name=team_name_unicode).first().__str__()))
                                except Exception as e:
                                    raise Exception('Error while parsing Teamname {}: {}'.format(team_name_raw, e.__str__()))
                            else:
                                print(u"Less than 5 columns, must be finals table or similar. --> ignore")
                    except Exception as e:
                        CrawlerLogMessage.objects.create(
                            message_type=CrawlerLogMessage.ERROR,
                            message=u"crawl_teams_per_league, {}".format(e.__str__())
                        )
        except Exception as e:
            print(u"exception {}")
            CrawlerLogMessage.objects.create(
                message_type=CrawlerLogMessage.ERROR,
                message=u"crawl_teams_per_league, {}".format(e.__str__())
            )
        if lock:
            with lock:
                self.statistics['teams'] += count
        else:
            self.statistics['teams'] += count

        return count

    def crawl_results(self, league_results_urls, deep_crawl=False):
        """
        Fetch all the results from a list of league urls.
        :param league_results_urls:    list of tuples [(league_shortcode, league_url), ..]
        :param deep_crawl:  defaults to False. Set True to follow pagination
        """
        for url in league_results_urls:
            self.crawl_results_per_league(url, deep_crawl)
        return self.statistics['results']

    def crawl_results_per_league(self, url, deep_crawl=False, lock=None):
        """
        Fetch all the results of a specific league.

        TODO: crawl also special tables like finals / semi finals
        :param url: the url of the league to crawl
        :param deep_crawl: follow pagination?
        :param lock:
        :return:
        """
        count = 0
        try:
            print(url)
            r = requests.get(url[1], headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            tables = soup.findAll('table', attrs={'class': 'table'})
            print(u"{} tables found.".format(len(tables)))
            competition = Competition.objects.get(id=url[2])

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        cells = row.findAll('td')
                        if len(cells) > 0:

                            # get host and guest team
                            teams = cells[2].find(text=True)        # teams
                            teams2 = teams.split(' - ')

                            host = Team.objects.filter(name=teams2[0].strip())
                            if not host:
                                logging.error(u"Hostteam not found: {}".format(teams2[0].strip()))
                                logging.error(row)
                                print(u"Hostteam not found: {}".format(teams2[0].strip()))
                                continue
                            else:
                                host = host[0]
                            guest = Team.objects.filter(name=teams2[1].strip())
                            if not guest:
                                logging.error(u"Guestteam not found: {}".format(teams2[1].strip()))
                                logging.error(row)
                                print(u"Guestteam not found: {}".format(teams2[1].strip()))
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

                            game.competition = competition
                            game.fsrID = cells[0].find(text=True)
                            game.fsrUrl = cells[0].find('a')['href']

                            # Game details & team logos

                            # make new request to game detail page
                            r2 = requests.get(game.fsrUrl, headers=self.headers)
                            soup2 = BeautifulSoup(r2.text, "html.parser")
                            table2 = soup2.find('table', attrs={'class': None})
                            rows = table2.findAll('tr')

                            if len(rows) > 1:
                                host.logo = rows[1].findAll('td')[0].find('img')['src']   # logo host
                                guest.logo = rows[1].findAll('td')[2].find('img')['src']  # logo guest

                                if len(rows) > 3:
                                    venueName = rows[3].findAll('td')[1].find(text=True)     # venue
                                    if not Venue.objects.filter(name=venueName):
                                        venue = Venue()
                                        venue.name = venueName
                                        print(u"Venue {} created".format(venueName))
                                    else:
                                        venue = Venue.objects.filter(name=venueName)[0]

                                scoreRow = 4

                                if len(rows) > scoreRow:
                                    if rows[scoreRow].findAll('td')[1].find(text=True).strip() == "Forfait":
                                        scoreRow += 1
                                        # save forfait in db
                                        if rows[scoreRow].findAll('td')[0].find(text=True).strip() != "":
                                            print("host forfait")
                                            hostParticipant.forfait = True
                                        elif rows[scoreRow].findAll('td')[2].find(text=True).strip() != "":
                                            print("guest forfait")
                                            guestParticipant.forfait = True

                                    hostParticipant.score = int(rows[scoreRow].findAll('td')[0].find(text=True))          # score host
                                    guestParticipant.score = int(rows[scoreRow].findAll('td')[2].find(text=True))         # score guest

                                    if len(rows) >= scoreRow+1:
                                        hostParticipant.tries = int(rows[scoreRow+1].findAll('td')[0].find(text=True))          # tries host
                                        guestParticipant.tries = int(rows[scoreRow+1].findAll('td')[2].find(text=True))         # tries guest
                                        if len(rows) >= scoreRow+2:
                                            hostParticipant.redCards = int(rows[scoreRow+2].findAll('td')[0].find(text=True))       # red cards host
                                            guestParticipant.redCards = int(rows[scoreRow+2].findAll('td')[2].find(text=True))      # red cards guest

                                            # referee is not always there
                                            if len(rows)>=scoreRow+5:
                                                refName = rows[scoreRow+4].findAll('td')[1].find(text=True).strip()     # referee
                                                # TODO: save performance by not reassigning referee if already set
                                                if not Referee.objects.filter(name=refName):
                                                    referee = Referee()
                                                    referee.name = refName
                                                    print(u"Referee {} created".format(refName))
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

                            print(u"GameResult {} created / updated".format(Game.objects.get(id=game.id).__str__()))

                            # increment game counter
                            count += 1

                    except Exception as e:
                        CrawlerLogMessage.objects.create(
                            message_type=CrawlerLogMessage.ERROR,
                            message=e.__str__()
                        )
            if deep_crawl:
                # recursively parse all next sites if there are any
                pagination = soup.find('div', attrs={'class': 'pagination'})
                if pagination:
                    current = pagination.find('span', attrs={'class': 'current'})
                    if current and int(current.find(text=True)) == 1:
                        print(u"Follow pagination, {} pages.".format(len(pagination)))
                        for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                            print(u"Page: {}, Current: {}".format(int(page.find(text=True)), int(current.find(text=True))))
                            if int(page.find(text=True)) > int(current.find(text=True)):
                                nextUrl = [(competition.league.shortcode, page['href'], competition.id)]
                                print(u"visit {}".format(nextUrl))
                                self.crawl_results(nextUrl)

        except Exception as e:
            CrawlerLogMessage.objects.create(
                message_type=CrawlerLogMessage.ERROR,
                message=e.__str__()
            )

        if lock:
            with lock:
                self.statistics['results'] += count
        else:
            self.statistics['results'] += count

        return count

    def crawl_fixtures(self, league_fixtures_urls, deep_crawl=False):
        """
        Fetch all the fixtures from the provided league urls.
        :param league_fixtures_urls: list of urls to fetch fixtures from
        :param deep_crawl: follow pagination?
        """
        for url in league_fixtures_urls:
            self.crawl_fixture_per_league(url, deep_crawl)
        return self.statistics['fixtures']


    def crawl_fixture_per_league(self, url, deep_crawl=False, lock=None):
        """
        Fetch all fixtures of a specific league.
        :param url: url to fetch fixtures from
        :param deep_crawl: deep_crawl: follow pagination?
        :param lock: ?
        :return: number of fetched fixtures
        """
        count = 0
        try:
            print(url)
            r = requests.get(url[1], headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find('table', attrs={'class': 'table'})
            competition = Competition.objects.get(id=url[2])

            for row in table.findAll('tr'):
                try:
                    cells = row.findAll('td')
                    if len(cells) > 0:

                        # get host and guest team
                        teams = cells[2].find(text=True)        # teams
                        teams2 = teams.split(' - ')

                        host = Team.objects.filter(name=teams2[0].strip())
                        if not host:
                            logging.error(u"Hostteam not found: ".format(teams2[0].strip()))
                            logging.error(row)
                            print(u"Hostteam not found: ".format(teams2[0].strip()))
                            continue
                        else:
                            host = host[0]
                        guest = Team.objects.filter(name=teams2[1].strip())
                        if not guest:
                            logging.error(u"Guestteam not found: ".format(teams2[1].strip()))
                            logging.error(row)
                            print(u"Guestteam not found: ".format(teams2[1].strip()))
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

                        game.competition = competition
                        game.fsrID = cells[0].find(text=True)
                        game.fsrUrl = cells[0].find('a')['href']

                        # Game details & team logos

                        # make new request to game detail page
                        r2 = requests.get(game.fsrUrl, headers=self.headers)
                        soup2 = BeautifulSoup(r2.text, "html.parser")
                        table2 = soup2.find('table', attrs={'class': None})
                        rows = table2.findAll('tr')

                        host.fsr_logo = rows[1].findAll('td')[0].find('img')['src']   # logo host
                        guest.fsr_logo = rows[1].findAll('td')[2].find('img')['src']  # logo guest
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

                        print(u"GameFixture {} created / updated".format(Game.objects.get(id=game.id)))

                        # increment game counter
                        count += 1

                except Exception as e:
                    CrawlerLogMessage.objects.create(
                        message_type=CrawlerLogMessage.ERROR,
                        message=e.__str__()
                    )
            if deep_crawl:
                # recursively parse all next sites if there are any
                pagination = soup.find('div', attrs={'class': 'pagination'})
                if pagination:
                    current = pagination.find('span', attrs={'class': 'current'})
                    if current and int(current.find(text=True)) == 1:
                        print(u"Follow pagination, {} pages.".format(len(pagination)))
                        for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                            if int(page.find(text=True)) > current:
                                nextUrl = [(competition.league.shortcode, page['href'], competition.id)]
                                self.crawl_fixtures(nextUrl)
        except Exception as e:
            CrawlerLogMessage.objects.create(
                message_type=CrawlerLogMessage.ERROR,
                message=e.__str__()
            )

        if lock:
            with lock:
                self.statistics['fixtures'] += count
        else:
            self.statistics['fixtures'] += count

        return count

