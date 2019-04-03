import sys

import requests
import rollbar
from bs4 import BeautifulSoup

from swissrugbystats.core.models import Game
from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogMixin import CrawlerLogMixin
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRGameParser import FSRGameParser


class GameCrawler(AbstractCrawler, CrawlerLogMixin):

    def start(self, game_id: int):
        self.log("""
------------------------------------------
Crawl Game by id {}
------------------------------------------
""".format(game_id), True, True)
        game = Game.objects.get(pk=game_id)
        if game:
            GameCrawler.crawl_single_url(game.fsrUrl)
        else:
            self.log("Game {} not found. Abort.".format(game_id))

        self.log("""
------------------------------------------
Game crawl ended successfully.
------------------------------------------
""".format(game_id), True, True)

    @classmethod
    def crawl_single_url(cls, url: str, competition: any = None, follow_pagination: bool = False) -> bool:
        """
        TODO: logs?
        :param url:
        :param competition:
        :param follow_pagination:
        :return:
        """
        logger = CrawlerLogger.get_logger_for_class(cls)

        try:
            logger.log("Crawl Game Details: " + url)

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
