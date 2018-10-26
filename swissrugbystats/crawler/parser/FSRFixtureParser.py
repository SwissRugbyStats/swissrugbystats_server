import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from swissrugbystats.core.models import Team, Game, GameParticipation, Venue
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser import FSRAbstractParser
from swissrugbystats.crawler.parser.FSRGameParser import FSRGameParser


class FSRFixtureParser(FSRAbstractParser):

    @staticmethod
    def parse_row(row, competition):
        """

        :param row:
        :return: boolean
        """
        logger = CrawlerLogger.get_logger_for_class(FSRFixtureParser)

        cells = row.findAll('td')
        if len(cells) > 0:

            # check if game is already stored, if so, update the existing one
            fsr_url = cells[0].find('a')['href']

            logger.log("Crawl Game Details: " + fsr_url);

            # Game details & team logos

            # make new request to game detail page
            r = requests.get(fsr_url, headers=FSRAbstractParser.get_request_headers())
            soup = BeautifulSoup(r.text, "html.parser")
            game_detail_table = soup.find('table', attrs={'class': None})

            rows = game_detail_table.findAll('tr')

            if FSRGameParser.parse_rows(rows, fsr_url):
                # logger.log(u"GameFixture {} created / updated".format(Game.objects.get(id=game.id)))
                # increment game counter
                return True
            else:
                return False


