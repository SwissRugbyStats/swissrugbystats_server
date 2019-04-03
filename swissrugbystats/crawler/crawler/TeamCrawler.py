import sys

import rollbar

from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRLeagueParser import FSRLeagueParser


class TeamCrawler(AbstractCrawler):

    @classmethod
    def crawl_by_url(cls, competition: Competition, url: str) -> int:
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        logger.log("crawl {}".format(competition.__str__()))
        try:
            tables = cls.get_tables(competition.get_league_url())

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        if FSRLeagueParser.parse_row(row, competition):
                            count = count + 1
                    except Exception as e:
                        logger.error(e)
                        rollbar.report_exc_info(sys.exc_info())

        except Exception as e:
            logger.error(e)
            rollbar.report_exc_info(sys.exc_info())

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['teams'] += count
        # else:
        #     self.statistics['teams'] += count

        return count

    @classmethod
    def crawl_competition(cls, competition: Competition, follow_pagination: bool = False) -> int:
        """
        Fetch all the teams that are participating in a league.
        :param competition:
        :param follow_pagination:
        :return:
        """
        return cls.crawl_by_url(competition, None)
