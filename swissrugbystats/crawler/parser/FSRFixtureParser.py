import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from swissrugbystats.core.models import Team, Game, GameParticipation, Venue
from swissrugbystats.crawler.parser import FSRAbstractParser


class FSRFixtureParser(FSRAbstractParser):

    @staticmethod
    def create_or_update(team):
        """

        :param team:
        :return:
        """
        pass

    @staticmethod
    def parse_row(row):
        """

        :param row:
        :return:
        """
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
                return
            else:
                host = host[0]
            guest = Team.objects.filter(name=teams2[1].strip())
            if not guest:
                logging.error(u"Guestteam not found: ".format(teams2[1].strip()))
                logging.error(row)
                print(u"Guestteam not found: ".format(teams2[1].strip()))
                return
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
            r2 = requests.get(game.fsrUrl, headers=FSRFixtureParser.get_request_headers())
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
            # count += 1
