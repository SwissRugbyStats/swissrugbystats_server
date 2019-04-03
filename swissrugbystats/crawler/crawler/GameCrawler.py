import sys

import requests
import rollbar
from bs4 import BeautifulSoup

from swissrugbystats.core.models import Game, Competition
from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogMixin import CrawlerLogMixin
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRGameParser import FSRGameParser


class GameCrawler(AbstractCrawler, CrawlerLogMixin):

    def start(self, game_id: int):
        """
        Crawl an existing game.
        :param game_id:
        :return:
        """
        self.log("""
------------------------------------------
Crawl Game by id {}
------------------------------------------
""".format(game_id), True, True)
        game = Game.objects.get(pk=game_id)
        if game:
            GameCrawler.crawl_by_url(game.competition, game.fsrUrl)
        else:
            self.log("Game {} not found. Abort.".format(game_id))

        self.log("""
------------------------------------------
Game crawl ended successfully.
------------------------------------------
""".format(game_id), True, True)

    @classmethod
    def crawl_competition(cls, competition: Competition, follow_pagination: bool = False) -> any:
        """
        Fetch all the teams that are participating in a league.
        :param competition:
        :param follow_pagination:
        :return:
        """
        raise NotImplementedError('GameCrawler has no crawl_competition implementation')

    @classmethod
    def crawl_by_url(cls, competition: Competition, url: str) -> bool:
        """
        TODO: logs?
        :param url:
        :param competition:
        :param follow_pagination:
        :return:
        """
        logger = CrawlerLogger.get_logger_for_class(cls)

        try:
            logger.log("Crawl Game Details: " + url + ". Competition: " + competition.__str__())

            # make new request to game detail page
            r = requests.get(url, headers=cls.get_request_headers())
            soup = BeautifulSoup(r.text, "html.parser")
            game_detail_table = soup.find('table', attrs={'class': None})

            rows = game_detail_table.findAll('tr')

            if FSRGameParser.parse_rows(rows, url, competition):
                return True

        except Exception as e:
            rollbar.report_exc_info(sys.exc_info())
            logger.log(e)

        return False
