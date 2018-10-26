import requests
from bs4 import BeautifulSoup

from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRGameParser import FSRGameParser


class GameCrawler(AbstractCrawler):

    @classmethod
    def crawl_single_url(cls, url, follow_pagination=False):
        """
        TODO: logs?
        :param url:
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

            if FSRGameParser.parse_rows(rows, url):
                return True

        except Exception as e:
            logger.log(e)

        return False
