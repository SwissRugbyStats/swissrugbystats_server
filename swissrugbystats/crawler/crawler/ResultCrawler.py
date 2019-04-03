import sys

import rollbar

from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRResultParser import FSRResultParser


class ResultCrawler(AbstractCrawler):

    @classmethod
    def crawl_by_url(cls, competition: Competition, url: str):
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        tables = cls.get_tables(url)

        for table in tables:
            for row in table.findAll('tr'):
                try:
                    if FSRResultParser.parse_row(row, competition):
                        count = count + 1

                except Exception as e:
                    rollbar.report_exc_info(sys.exc_info())
                    logger.error(e)

        return count

    @classmethod
    def crawl_competition(cls, competition: Competition, follow_pagination: bool = False) -> any:
        # (cls, url: (str, str, int), follow_pagination: bool = False) -> int:
        """
        Fetch all the results of a specific league.

        TODO: crawl also special tables like finals / semi finals
        :param competition: the url of the league to crawl
        :param follow_pagination: follow pagination?
        :return:
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)
        url = competition.get_results_url()

        try:
            logger.log("crawl per league {}".format(url))

            count = cls.crawl_by_url(competition, url)

            if follow_pagination:
                count = count + cls.follow_pagination(url, competition)

        except Exception as e:
            rollbar.report_exc_info(sys.exc_info())
            logger.error(e)

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['results'] += count
        # else:
        #     self.statistics['results'] += count

        return count
