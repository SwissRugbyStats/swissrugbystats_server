import sys

import rollbar

from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRFixtureParser import FSRFixtureParser


class FixtureCrawler(AbstractCrawler):

    @classmethod
    def crawl_by_url(cls, competition: Competition, url: str) -> int:
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        table = cls.get_table(url)

        for row in table.findAll('tr'):
            try:
                if FSRFixtureParser.parse_row(row, competition):
                    count = count + 1

            except Exception as e:
                logger.error(e)
                rollbar.report_exc_info(sys.exc_info())

        return count

    @classmethod
    def crawl_competition(cls, competition: Competition, follow_pagination: bool = False) -> int:
        """
        Fetch all the teams that are participating in a league.
        :param competition:
        :param follow_pagination:
        :return:
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)
        url = competition.get_fixtures_url()

        try:
            logger.log("crawl per league {}".format(url))

            count = count + cls.crawl_by_url(competition, url)

            if follow_pagination:
                count = count + cls.follow_pagination(competition, url)

        except Exception as e:
            logger.error(e)
            rollbar.report_exc_info(sys.exc_info())

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['fixtures'] += count
        # else:
        #     self.statistics['fixtures'] += count

        return count
