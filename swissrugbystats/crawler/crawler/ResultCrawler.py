from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser import FSRAbstractParser, FSRResultParser


class ResultCrawler(AbstractCrawler):

    @classmethod
    def crawl_single_url(cls, url, follow_pagination=False):
        """
        Fetch all the results of a specific league.

        TODO: crawl also special tables like finals / semi finals
        :param url: the url of the league to crawl
        :param follow_pagination: follow pagination?
        :return:
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        try:
            logger.log("crawl per league {}".format(url))
            tables = FSRAbstractParser.get_tables(url)
            competition = Competition.objects.get(id=url[2])

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        if FSRResultParser.parse_row(row, competition):
                            count = count + 1

                    except Exception as e:
                        logger.error(e)

            if follow_pagination:
                count = count + ResultCrawler.follow_pagination(url, competition)

        except Exception as e:
            logger.error(e)

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['results'] += count
        # else:
        #     self.statistics['results'] += count

        return count
