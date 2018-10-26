from swissrugbystats.crawler.crawler.GameCrawler import GameCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRAbstractParser import FSRAbstractParser


class FSRFixtureParser(FSRAbstractParser):

    @staticmethod
    def parse_row(row, competition=None):
        """

        :param row:
        :param competition:
        :return: boolean
        """
        logger = CrawlerLogger.get_logger_for_class(FSRFixtureParser)

        try:

            cells = row.findAll('td')
            if len(cells) > 0:
                # check if game is already stored, if so, update the existing one
                fsr_url = cells[0].find('a')['href']

                return GameCrawler.crawl_single_url(fsr_url)

        except Exception as e:
            logger.error(e)

        return False
