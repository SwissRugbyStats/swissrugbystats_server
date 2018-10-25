from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser import FSRAbstractParser, FSRFixtureParser


class FixtureCrawler(AbstractCrawler):

    @classmethod
    def crawl_per_league(cls, url, follow_pagination=False):
        """
            Fetch all fixtures of a specific league.
            :param url: url to fetch fixtures from
            :param deep_crawl: deep_crawl: follow pagination?
            :param lock: ?
            :return: number of fetched fixtures
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        try:
            logger.log("crawl per league {}".format(url))
            table = FSRAbstractParser.get_table(url)
            competition = Competition.objects.get(id=url[2])

            for row in table.findAll('tr'):
                try:
                    if FSRFixtureParser.parse_row(row, competition):
                        count = count + 1

                except Exception as e:
                    logger.error(e)
            if follow_pagination:
                count = count + FixtureCrawler.follow_pagination(url, competition)

        except Exception as e:
            logger.error(e)

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['fixtures'] += count
        # else:
        #     self.statistics['fixtures'] += count

        return count