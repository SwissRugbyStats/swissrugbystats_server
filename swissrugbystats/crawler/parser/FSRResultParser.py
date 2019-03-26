from swissrugbystats.crawler.crawler.GameCrawler import GameCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRAbstractParser import FSRAbstractParser


class FSRResultParser(FSRAbstractParser):

    @staticmethod
    def parse_row(row: str, competition: int = None) -> bool:
        """

        :param row:
        :param competition:
        :return:
        """
        logger = CrawlerLogger.get_logger_for_class(FSRResultParser)

        try:
            cells = row.findAll('td')
            if len(cells) > 0:
                # check if game is already stored, if so, update the existing one
                fsr_url = cells[0].find('a')['href']

                return GameCrawler.crawl_single_url(fsr_url)

        except Exception as e:
            logger.error(e)
